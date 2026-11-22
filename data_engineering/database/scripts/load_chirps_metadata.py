
import os
import glob
import rasterio
import numpy as np
import psycopg2

from pathlib import Path
from datetime import datetime
from psycopg2.extras import execute_values
from data_engineering.database.db_config import DB_CONFIG

INPUT_DIR = "data/processed/chirps/daily"



print("CHIRPS RASTER METADATA LOADING")
print("=" * 45)

# 1. Find raster files
files = sorted(
    glob.glob(os.path.join(INPUT_DIR, "*.tif"))
)

print(f"Source files: {len(files)}")

if len(files) != 30:
    raise ValueError(
        f"Expected 30 raster files, found {len(files)}"
    )

# 2. Read and validate raster metadata
records = []

for file_path in files:

    with rasterio.open(file_path) as src:

        if src.crs is None or src.crs.to_epsg() != 4326:
            raise ValueError(
                f"Invalid CRS: {file_path}"
            )

        if src.count != 1:
            raise ValueError(
                f"Unexpected band count: {file_path}"
            )

        if src.nodata is None:
            raise ValueError(
                f"NoData value missing: {file_path}"
            )

        if src.width != 210 or src.height != 188:
            raise ValueError(
                f"Unexpected raster dimensions: {file_path}"
            )

        if src.nodata != -9999:
            raise ValueError(
                f"Unexpected NoData value: {file_path}"
            )

        # Extract date from filename
        filename = os.path.basename(file_path)

        date_string = filename.replace(
            "chirps-v3.0.sat.", ""
        ).replace(".tif", "")

        raster_date = datetime.strptime(
            date_string, "%Y.%m.%d"
        ).date()

        # Read raster values, excluding NoData
        data = src.read(1, masked=True)

        if data.count() == 0:
            raise ValueError(
                f"Raster contains no valid pixels: {filename}"
            )

        min_value = float(data.min())
        max_value = float(data.max())
        mean_value = float(data.mean())

        # Store relative path for portability
        relative_path = Path(file_path).as_posix()

        records.append((
            raster_date,
            filename,
            relative_path,
            src.crs.to_string(),
            src.width,
            src.height,
            src.count,
            float(src.res[0]),
            float(src.res[1]),
            float(src.nodata),
            min_value,
            max_value,
            mean_value
        ))

print(f"Prepared records: {len(records)}")
print("Raster validation completed.")

# 3. Load metadata into PostgreSQL
connection = None

try:
    connection = psycopg2.connect(**DB_CONFIG)

    with connection:
        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT COUNT(*)
                FROM karhutla.chirps_raster_metadata;
            """)

            existing_count = cursor.fetchone()[0]

            if existing_count > 0:
                raise ValueError(
                    "CHIRPS metadata table is not empty. "
                    "Loading cancelled to avoid duplicates."
                )

            execute_values(
                cursor,
                """
                INSERT INTO karhutla.chirps_raster_metadata (
                    raster_date,
                    file_name,
                    file_path,
                    crs,
                    width,
                    height,
                    band_count,
                    resolution_x,
                    resolution_y,
                    nodata_value,
                    min_value,
                    max_value,
                    mean_value
                )
                VALUES %s
                """,
                records,
                page_size=30
            )

    print("CHIRPS metadata loading completed successfully.")

except Exception as error:
    print(f"ERROR: {error}")
    raise

finally:
    if connection:
        connection.close()

# 4. Validate database results
connection = psycopg2.connect(**DB_CONFIG)

try:
    with connection.cursor() as cursor:

        cursor.execute("""
            SELECT
                COUNT(*),
                COUNT(DISTINCT raster_date),
                COUNT(DISTINCT file_name),
                MIN(raster_date),
                MAX(raster_date),
                MIN(min_value),
                MAX(max_value),
                ROUND(AVG(mean_value)::numeric, 4)
            FROM karhutla.chirps_raster_metadata;
        """)

        result = cursor.fetchone()

        print("\nDATABASE VALIDATION")
        print("=" * 45)
        print(f"Total records: {result[0]}")
        print(f"Unique dates: {result[1]}")
        print(f"Unique filenames: {result[2]}")
        print(f"First raster date: {result[3]}")
        print(f"Last raster date: {result[4]}")
        print(f"Minimum raster value: {result[5]}")
        print(f"Maximum raster value: {result[6]}")
        print(f"Average of daily means: {result[7]}")

finally:
    connection.close()
