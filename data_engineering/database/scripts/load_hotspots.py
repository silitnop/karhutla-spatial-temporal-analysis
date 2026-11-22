
import pandas as pd
import psycopg2

from psycopg2.extras import execute_values


INPUT_FILE = (
    "data/processed/firms/"
    "hotspots_kalimantan_september_2026.csv"
)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "karhutla_db",
    "user": "postgres",
    "password": "Silit123"
}


print("FIRMS HOTSPOT DATA LOADING")
print("=" * 45)

# 1. Read source data
df = pd.read_csv(INPUT_FILE)

print(f"Source records: {len(df)}")

# 2. Validate source data
if df.isna().any().any():
    raise ValueError("NULL values found in source data")

if not df["province"].isin([
    "Kalimantan Barat",
    "Kalimantan Selatan",
    "Kalimantan Tengah",
    "Kalimantan Timur",
    "Kalimantan Utara"
]).all():
    raise ValueError("Unexpected province name found")

if not df["latitude"].between(-90, 90).all():
    raise ValueError("Invalid latitude values")

if not df["longitude"].between(-180, 180).all():
    raise ValueError("Invalid longitude values")

if (df["frp"] < 0).any():
    raise ValueError("Negative FRP values found")

# 3. Convert acquisition date
df["acq_date"] = pd.to_datetime(
    df["acq_date"],
    errors="raise"
).dt.date

print("Source validation completed.")

# 4. Connect to PostgreSQL
connection = None

try:
    connection = psycopg2.connect(**DB_CONFIG)

    with connection:
        with connection.cursor() as cursor:

            # Check target table
            cursor.execute("""
                SELECT COUNT(*)
                FROM karhutla.fact_hotspots;
            """)

            existing_count = cursor.fetchone()[0]

            if existing_count > 0:
                raise ValueError(
                    "Hotspot table is not empty. "
                    "Loading cancelled to avoid duplicates."
                )

            # Get province ID mapping
            cursor.execute("""
                SELECT province_id, province_name
                FROM karhutla.dim_provinces;
            """)

            province_mapping = {
                name: province_id
                for province_id, name in cursor.fetchall()
            }

            # Verify all provinces exist
            missing_provinces = (
                set(df["province"].unique())
                - set(province_mapping.keys())
            )

            if missing_provinces:
                raise ValueError(
                    f"Province not found in database: "
                    f"{missing_provinces}"
                )

            # 5. Prepare records
            records = []

            for row in df.itertuples(index=False):

                province_id = province_mapping[row.province]

                records.append((
                    row.latitude,
                    row.longitude,
                    row.brightness,
                    row.scan,
                    row.track,
                    row.acq_date,
                    row.acq_time,
                    row.satellite,
                    row.instrument,
                    row.confidence,
                    row.version,
                    row.bright_t31,
                    row.frp,
                    row.daynight,
                    province_id,
                    row.longitude,
                    row.latitude
                ))

            print(f"Prepared records: {len(records)}")

            # 6. Insert records in batches
            execute_values(
                cursor,
                """
                INSERT INTO karhutla.fact_hotspots (
                    latitude,
                    longitude,
                    brightness,
                    scan,
                    track,
                    acq_date,
                    acq_time,
                    satellite,
                    instrument,
                    confidence,
                    version,
                    bright_t31,
                    frp,
                    daynight,
                    province_id,
                    geom
                )
                VALUES %s
                """,
                records,
                template="""
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    ST_SetSRID(
                        ST_MakePoint(%s, %s),
                        4326
                    )
                )
                """,
                page_size=5000
            )

    print("Hotspot loading completed successfully.")

except Exception as error:
    print(f"ERROR: {error}")
    raise

finally:
    if connection:
        connection.close()


# 7. Validate database results
connection = psycopg2.connect(**DB_CONFIG)

try:
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                COUNT(*),
                COUNT(DISTINCT hotspot_id),
                COUNT(*) FILTER (
                    WHERE ST_GeometryType(geom) = 'ST_Point'
                ),
                COUNT(*) FILTER (
                    WHERE ST_SRID(geom) = 4326
                ),
                MIN(acq_date),
                MAX(acq_date)
            FROM karhutla.fact_hotspots;
        """)

        result = cursor.fetchone()

        print("\nDATABASE VALIDATION")
        print("=" * 45)
        print(f"Total records: {result[0]}")
        print(f"Unique hotspot IDs: {result[1]}")
        print(f"Point geometries: {result[2]}")
        print(f"Geometry with SRID 4326: {result[3]}")
        print(f"First acquisition date: {result[4]}")
        print(f"Last acquisition date: {result[5]}")

        cursor.execute("""
            SELECT
                p.province_name,
                COUNT(h.hotspot_id)
            FROM karhutla.dim_provinces p
            LEFT JOIN karhutla.fact_hotspots h
                ON p.province_id = h.province_id
            GROUP BY p.province_id, p.province_name
            ORDER BY p.province_name;
        """)

        print("\nHOTSPOTS BY PROVINCE")
        print("=" * 45)

        for province, total in cursor.fetchall():
            print(f"{province}: {total}")

finally:
    connection.close()
