
import geopandas as gpd
import psycopg2

from psycopg2.extras import execute_values
from shapely import force_2d


INPUT_FILE = (
    "data/staging/sentinel2/"
    "sentinel2_september_2026_footprints.geojson"
)

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "karhutla_db",
    "user": "postgres",
    "password": "Silit123"
}


print("SENTINEL-2 DATA LOADING")
print("=" * 45)

# 1. Read source data
gdf = gpd.read_file(INPUT_FILE)

print(f"Source records: {len(gdf)}")
print(f"Source CRS: {gdf.crs}")

# 2. Validate source data
required_columns = [
    "product_id",
    "datetime",
    "cloud_cover",
    "mgrs_tile",
    "platform",
    "instruments",
    "processing_level",
    "collection",
    "geometry"
]

missing_columns = set(required_columns) - set(gdf.columns)

if missing_columns:
    raise ValueError(f"Missing columns: {missing_columns}")

if gdf.crs is None or gdf.crs.to_epsg() != 4326:
    raise ValueError("Dataset CRS must be EPSG:4326")

if gdf[required_columns[:-1]].isna().any().any():
    raise ValueError("NULL values found in metadata")

if gdf["product_id"].duplicated().any():
    raise ValueError("Duplicate product_id found")

if not gdf.geometry.is_valid.all():
    raise ValueError("Invalid geometry found")

if gdf.geometry.is_empty.any():
    raise ValueError("Empty geometry found")

if not gdf.geometry.geom_type.eq("Polygon").all():
    raise ValueError("All geometries must be Polygon")

if not gdf["cloud_cover"].between(0, 100).all():
    raise ValueError("Invalid cloud cover values")

print("Source validation completed.")

# 3. Prepare records
records = []

for _, row in gdf.iterrows():

    geometry = force_2d(row.geometry)

    if geometry.geom_type != "Polygon":
        raise ValueError(
            f"Unexpected geometry: {geometry.geom_type}"
        )

    instruments = row["instruments"]

    if isinstance(instruments, (list, tuple)):
        instruments = ", ".join(str(x) for x in instruments)
    else:
        instruments = str(instruments)

    acquisition_datetime = row["datetime"]

    records.append((
        str(row["product_id"]),
        acquisition_datetime.to_pydatetime(),
        float(row["cloud_cover"]),
        str(row["mgrs_tile"]),
        str(row["platform"]),
        instruments,
        str(row["processing_level"]),
        str(row["collection"]),
        geometry.wkt
    ))

print(f"Prepared records: {len(records)}")

# 4. Load into PostgreSQL
connection = None

try:
    connection = psycopg2.connect(**DB_CONFIG)

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*)
                FROM karhutla.sentinel2_products;
            """)

            existing_count = cursor.fetchone()[0]

            if existing_count > 0:
                raise ValueError(
                    "Sentinel-2 table is not empty. "
                    "Loading cancelled to avoid duplicates."
                )

            execute_values(
                cursor,
                """
                INSERT INTO karhutla.sentinel2_products (
                    product_id,
                    acquisition_datetime,
                    cloud_cover,
                    mgrs_tile,
                    platform,
                    instruments,
                    processing_level,
                    collection,
                    geom
                )
                VALUES %s
                """,
                records,
                template="""
                (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s,
                    ST_GeomFromText(%s, 4326)
                )
                """,
                page_size=1000
            )

    print("Sentinel-2 loading completed successfully.")

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
                COUNT(DISTINCT product_id),
                COUNT(*) FILTER (
                    WHERE ST_GeometryType(geom) = 'ST_Polygon'
                ),
                COUNT(*) FILTER (
                    WHERE ST_SRID(geom) = 4326
                ),
                MIN(acquisition_datetime),
                MAX(acquisition_datetime),
                ROUND(AVG(cloud_cover)::numeric, 2)
            FROM karhutla.sentinel2_products;
        """)

        result = cursor.fetchone()

        print("\nDATABASE VALIDATION")
        print("=" * 45)
        print(f"Total records: {result[0]}")
        print(f"Unique product IDs: {result[1]}")
        print(f"Polygon geometries: {result[2]}")
        print(f"Geometry with SRID 4326: {result[3]}")
        print(f"First acquisition: {result[4]}")
        print(f"Last acquisition: {result[5]}")
        print(f"Average cloud cover: {result[6]}%")

finally:
    connection.close()
