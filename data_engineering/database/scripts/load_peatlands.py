
import geopandas as gpd
import psycopg2
import pandas as pd
from data_engineering.database.db_config import DB_CONFIG
from psycopg2.extras import execute_values
from shapely import force_2d
from shapely.geometry import MultiPolygon


INPUT_FILE = (
    "data/processed/peatland/"
    "peatland_kalimantan_clean.geojson"
)



print("PEATLAND DATA LOADING")
print("=" * 40)

# 1. Read source data
gdf = gpd.read_file(INPUT_FILE)

print(f"Source records: {len(gdf)}")
print(f"Source CRS: {gdf.crs}")

# 2. Validate source data
if gdf.crs is None or gdf.crs.to_epsg() != 4326:
    raise ValueError("Dataset CRS must be EPSG:4326")

if gdf["objectid"].isna().any():
    raise ValueError("objectid contains NULL values")

if gdf["objectid"].duplicated().any():
    raise ValueError("Duplicate objectid found")

if gdf.geometry.isna().any() or gdf.geometry.is_empty.any():
    raise ValueError("Null or empty geometry found")

if not gdf.geometry.is_valid.all():
    raise ValueError("Invalid geometry found in source data")

# 3. Prepare records
records = []

for _, row in gdf.iterrows():

    geometry = force_2d(row.geometry)

    if geometry.geom_type == "Polygon":
        geometry = MultiPolygon([geometry])

    if geometry.geom_type != "MultiPolygon":
        raise ValueError(
            f"Unexpected geometry type: {geometry.geom_type}"
        )

    records.append((
        int(row["objectid"]),
        int(row["OBJECTID_12"]),
        int(row["objectid_1"]),
        row["layer_revi"],
        row["layer_revi_clean"],
        row["globalid"],
        float(row["Shape_Length"]),
        float(row["Shape_Area"]),
        geometry.wkt
    ))

print(f"Prepared records: {len(records)}")

# 4. Load data into PostgreSQL
connection = None

try:
    connection = psycopg2.connect(**DB_CONFIG)

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*)
                FROM karhutla.dim_peatlands;
            """)

            existing_count = cursor.fetchone()[0]

            if existing_count > 0:
                raise ValueError(
                    "Peatland table is not empty. "
                    "Loading cancelled to avoid duplicates."
                )

            execute_values(
                cursor,
                """
                INSERT INTO karhutla.dim_peatlands (
                    peatland_id,
                    source_objectid_12,
                    source_objectid_1,
                    layer_revi,
                    layer_revi_clean,
                    globalid,
                    shape_length,
                    shape_area,
                    geom
                )
                VALUES %s
                """,
                records,
                template="""
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    ST_Multi(ST_GeomFromText(%s, 4326))
                )
                """
            )

    print("Peatland loading completed successfully.")

except Exception as error:
    print(f"ERROR: {error}")
    raise

finally:
    if connection:
        connection.close()


# 5. Validate database results
connection = psycopg2.connect(**DB_CONFIG)

try:
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                COUNT(*),
                COUNT(DISTINCT peatland_id),
                COUNT(*) FILTER (
                    WHERE ST_GeometryType(geom) = 'ST_MultiPolygon'
                ),
                COUNT(*) FILTER (
                    WHERE ST_SRID(geom) = 4326
                )
            FROM karhutla.dim_peatlands;
        """)

        result = cursor.fetchone()

        print("\nDATABASE VALIDATION")
        print("=" * 40)
        print(f"Total records: {result[0]}")
        print(f"Unique peatland IDs: {result[1]}")
        print(f"MultiPolygon geometries: {result[2]}")
        print(f"Geometry with SRID 4326: {result[3]}")

finally:
    connection.close()
