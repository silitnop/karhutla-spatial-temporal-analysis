
import geopandas as gpd
import psycopg2
from psycopg2.extras import execute_values
from shapely import force_2d
from data_engineering.database.db_config import DB_CONFIG

# ==========================================
# CONFIGURATION
# ==========================================

INPUT_FILE = (
    "data/processed/boundaries/"
    "kalimantan_provinces.geojson"
)


# ==========================================
# READ DATA
# ==========================================

print("PROVINCE DATA LOADING")
print("=" * 40)

gdf = gpd.read_file(INPUT_FILE)

print(f"Source records: {len(gdf)}")
print(f"Source CRS: {gdf.crs}")

if gdf.crs is None or gdf.crs.to_epsg() != 4326:
    raise ValueError("Dataset CRS must be EPSG:4326")

if gdf["wadmpr"].isna().any():
    raise ValueError("Province name contains NULL values")

if gdf.geometry.isna().any() or gdf.geometry.is_empty.any():
    raise ValueError("Invalid or empty geometry found")

# ==========================================
# PREPARE DATA
# ==========================================

records = []

for _, row in gdf.iterrows():
    province_name = row["wadmpr"]
    geometry = row.geometry

    if geometry.geom_type == "Polygon":
        geometry = geometry.__class__([geometry])

    if geometry.geom_type != "MultiPolygon":
        raise ValueError(
            f"Unexpected geometry type: {geometry.geom_type}"
        )

    geometry_2d = force_2d(geometry)

    records.append((
        province_name,
        geometry_2d.wkt
    ))

# ==========================================
# LOAD TO POSTGRESQL
# ==========================================

connection = None

try:
    connection = psycopg2.connect(**DB_CONFIG)

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*)
                FROM karhutla.dim_provinces;
            """)

            existing_count = cursor.fetchone()[0]

            if existing_count > 0:
                raise ValueError(
                    "Province table is not empty. "
                    "Loading cancelled to avoid duplicates."
                )

            execute_values(
                cursor,
                """
                INSERT INTO karhutla.dim_provinces
                    (province_name, geom)
                VALUES %s
                """,
                records,
                template="(%s, ST_Multi(ST_GeomFromText(%s, 4326)))"
            )

    print("Province loading completed successfully.")

except Exception as error:
    print(f"ERROR: {error}")
    raise

finally:
    if connection:
        connection.close()

# ==========================================
# VALIDATION
# ==========================================

connection = psycopg2.connect(**DB_CONFIG)

try:
    with connection.cursor() as cursor:
        cursor.execute("""
            SELECT
                province_id,
                province_name,
                ST_GeometryType(geom),
                ST_SRID(geom)
            FROM karhutla.dim_provinces
            ORDER BY province_id;
        """)

        results = cursor.fetchall()

        print("\nDATABASE VALIDATION")
        print("=" * 40)

        for result in results:
            print(result)

        print(f"\nTotal loaded provinces: {len(results)}")

finally:
    connection.close()
