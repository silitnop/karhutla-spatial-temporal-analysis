
# ==========================================
# SENTINEL-2 DATA DISCOVERY
# Project: Karhutla Spatial-Temporal Analysis
# Source: Copernicus Data Space Ecosystem
# ==========================================

import geopandas as gpd
import pandas as pd
import json
import requests
import time

from pathlib import Path
from shapely.geometry import shape


# ==========================================
# 1. PROJECT CONFIGURATION
# ==========================================

PROJECT_ROOT = Path.cwd()

BOUNDARY_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "boundaries"
    / "kalimantan_provinces.geojson"
)

RAW_DIR = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "sentinel2"
)

STAGING_DIR = (
    PROJECT_ROOT
    / "data"
    / "staging"
    / "sentinel2"
)

RAW_DIR.mkdir(parents=True, exist_ok=True)
STAGING_DIR.mkdir(parents=True, exist_ok=True)


# ==========================================
# 2. SEARCH CONFIGURATION
# ==========================================

STAC_URL = "https://stac.dataspace.copernicus.eu/v1"

COLLECTION = "sentinel-2-l2a"

START_DATE = "2026-09-01T00:00:00Z"
END_DATE = "2026-09-30T23:59:59Z"

MAX_CLOUD_COVER = 30

MAX_RETRIES = 3
REQUEST_TIMEOUT = 180


# ==========================================
# 3. LOAD STUDY AREA
# ==========================================

print("\n===== LOAD STUDY AREA =====")

if not BOUNDARY_PATH.exists():
    raise FileNotFoundError(
        f"Boundary file not found: {BOUNDARY_PATH}"
    )

boundaries = gpd.read_file(BOUNDARY_PATH)

if boundaries.empty:
    raise ValueError("Boundary dataset is empty.")

if boundaries.crs is None:
    raise ValueError("Boundary CRS is undefined.")

boundaries = boundaries.to_crs("EPSG:4326")

if not boundaries.geometry.is_valid.all():
    raise ValueError("Invalid boundary geometry detected.")

study_area = boundaries.geometry.union_all()

if study_area.is_empty:
    raise ValueError("Study area geometry is empty.")

print("Total provinces:", len(boundaries))
print("CRS:", boundaries.crs)
print("Geometry type:", study_area.geom_type)
print("Geometry valid:", study_area.is_valid)
print("Bounding box:", boundaries.total_bounds)


# ==========================================
# 4. SEARCH SENTINEL-2 PRODUCTS
# ==========================================

print("\n===== SEARCH SENTINEL-2 PRODUCTS =====")

search_url = f"{STAC_URL}/search"

minx, miny, maxx, maxy = boundaries.total_bounds

payload = {
    "collections": [COLLECTION],
    "bbox": [
        float(minx),
        float(miny),
        float(maxx),
        float(maxy)
    ],
    "datetime": f"{START_DATE}/{END_DATE}",
    "query": {
        "eo:cloud_cover": {
            "lte": MAX_CLOUD_COVER
        }
    },
    "limit": 100
}

all_features = []

next_url = search_url
next_payload = payload.copy()

page = 1

while next_url:

    response = None

    # Retry request if server timeout occurs
    for attempt in range(1, MAX_RETRIES + 1):

        try:
            response = requests.post(
                next_url,
                json=next_payload,
                timeout=REQUEST_TIMEOUT
            )

            response.raise_for_status()
            break

        except requests.exceptions.RequestException as error:

            if attempt == MAX_RETRIES:
                raise

            wait_time = attempt * 10

            print(
                f"Request failed "
                f"(attempt {attempt}/{MAX_RETRIES}): {error}"
            )

            print(f"Retrying in {wait_time} seconds...")

            time.sleep(wait_time)

    result = response.json()

    features = result.get("features", [])

    all_features.extend(features)

    print(f"Page {page}: {len(features)} products")

    next_link = next(
        (
            link
            for link in result.get("links", [])
            if link.get("rel") == "next"
        ),
        None
    )

    if next_link:

        next_url = next_link["href"]
        next_payload = next_link.get("body", {})

    else:

        next_url = None

    page += 1


if not all_features:
    raise ValueError(
        "No Sentinel-2 products found from STAC search."
    )


# ==========================================
# 5. SAVE RAW STAC RESPONSE
# ==========================================

print("\n===== SAVE RAW STAC RESPONSE =====")

raw_catalog_path = (
    RAW_DIR
    / "sentinel2_september_2026_stac_search.geojson"
)

raw_collection = {
    "type": "FeatureCollection",
    "features": all_features
}

with raw_catalog_path.open("w", encoding="utf-8") as file:

    json.dump(
        raw_collection,
        file,
        ensure_ascii=False
    )

print("Raw STAC response saved:", raw_catalog_path)
print("Raw STAC features:", len(all_features))


# ==========================================
# 6. FILTER PRODUCTS BY STUDY AREA
# ==========================================

print("\n===== FILTER PRODUCTS BY STUDY AREA =====")

filtered_features = []

for feature in all_features:

    geometry = feature.get("geometry")

    if geometry is None:
        continue

    footprint = shape(geometry)

    if footprint.intersects(study_area):
        filtered_features.append(feature)

print("Products from bounding box:", len(all_features))

print(
    "Products intersecting Kalimantan:",
    len(filtered_features)
)

items = filtered_features

print("Total products found:", len(items))

if not items:
    raise ValueError(
        "No Sentinel-2 products intersect the study area."
    )


# ==========================================
# 7. EXTRACT PRODUCT METADATA
# ==========================================

print("\n===== EXTRACT PRODUCT METADATA =====")

records = []

for item in items:

    props = item.get("properties", {})

    grid_code = props.get("grid:code")

    mgrs_tile = (
        grid_code.replace("MGRS-", "")
        if grid_code else None
    )

    records.append({

        "product_id": item.get("id"),

        "datetime": props.get("datetime"),

        "cloud_cover": props.get("eo:cloud_cover"),

        "mgrs_tile": mgrs_tile,

        "platform": props.get("platform"),

        "instruments": props.get("instruments"),

        "processing_level": props.get("processing:level"),

        "collection": item.get("collection"),

        "bbox": item.get("bbox"),

        "geometry": item.get("geometry")

    })

metadata = pd.DataFrame(records)

if metadata.empty:
    raise ValueError("Extracted metadata is empty.")

print("Metadata records:", len(metadata))

print(
    "Unique products:",
    metadata["product_id"].nunique()
)

print(
    "Unique tiles:",
    metadata["mgrs_tile"].nunique()
)


# ==========================================
# 8. DATA QUALITY CHECK
# ==========================================

print("\n===== DATA QUALITY CHECK =====")

print(
    "Missing product ID:",
    metadata["product_id"].isna().sum()
)

print(
    "Missing datetime:",
    metadata["datetime"].isna().sum()
)

print(
    "Missing cloud cover:",
    metadata["cloud_cover"].isna().sum()
)

print("\nCloud cover statistics:")

print(metadata["cloud_cover"].describe())

print("\nProducts by tile:")

print(
    metadata["mgrs_tile"].value_counts(dropna=False)
)


# ==========================================
# 9. SORT PRODUCTS
# ==========================================

metadata_sorted = metadata.sort_values(
    by=["cloud_cover", "datetime"],
    ascending=[True, True]
).reset_index(drop=True)

print("\n===== TOP 20 PRODUCTS =====")

print(
    metadata_sorted[
        [
            "product_id",
            "datetime",
            "cloud_cover",
            "mgrs_tile"
        ]
    ].head(20).to_string(index=False)
)


# ==========================================
# 10. GENERATE TILE SUMMARY
# ==========================================

print("\n===== TILE SUMMARY =====")

tile_summary = (

    metadata.groupby("mgrs_tile", dropna=False)

    .agg(

        total_products=("product_id", "count"),

        min_cloud_cover=("cloud_cover", "min"),

        mean_cloud_cover=("cloud_cover", "mean"),

        max_cloud_cover=("cloud_cover", "max"),

        first_date=("datetime", "min"),

        last_date=("datetime", "max")

    )

    .sort_values("min_cloud_cover")

)

print(tile_summary.to_string())


# ==========================================
# 11. SAVE METADATA AND TILE SUMMARY
# ==========================================

print("\n===== SAVE STAGING OUTPUTS =====")

metadata_path = (
    STAGING_DIR
    / "sentinel2_september_2026_metadata.csv"
)

summary_path = (
    STAGING_DIR
    / "sentinel2_september_2026_tile_summary.csv"
)

metadata_sorted.drop(
    columns=["geometry", "bbox"]
).to_csv(
    metadata_path,
    index=False
)

tile_summary.to_csv(
    summary_path
)

print("Metadata saved:", metadata_path)
print("Tile summary saved:", summary_path)


# ==========================================
# 12. SAVE PRODUCT FOOTPRINTS
# ==========================================

print("\n===== SAVE PRODUCT FOOTPRINTS =====")

footprint_geometries = metadata["geometry"].apply(

    lambda geom: (
        shape(geom)
        if isinstance(geom, dict)
        else None
    )

)

footprints = gpd.GeoDataFrame(

    metadata.drop(
        columns=["bbox", "geometry"]
    ),

    geometry=footprint_geometries,

    crs="EPSG:4326"

)

# Remove records with missing geometry
footprints = footprints[
    footprints.geometry.notna()
].copy()

# Validate geometries
missing_geometries = footprints.geometry.isna().sum()

invalid_geometries = (
    ~footprints.geometry.is_valid
).sum()

print("Missing geometries:", missing_geometries)

print("Invalid geometries:", invalid_geometries)

footprint_path = (
    STAGING_DIR
    / "sentinel2_september_2026_footprints.geojson"
)

footprints.to_file(
    footprint_path,
    driver="GeoJSON"
)

print("Footprints saved:", len(footprints))


# ==========================================
# 13. FINAL VALIDATION
# ==========================================

print("\n===== FINAL VALIDATION =====")

print("Raw catalog exists:", raw_catalog_path.exists())

print("Metadata exists:", metadata_path.exists())

print("Tile summary exists:", summary_path.exists())

print("Footprints exist:", footprint_path.exists())

print("Raw STAC features:", len(all_features))

print("Filtered metadata rows:", len(metadata_sorted))

print(
    "Unique products:",
    metadata_sorted["product_id"].nunique()
)

print(
    "Unique tiles:",
    metadata_sorted["mgrs_tile"].nunique()
)

print("Footprint features:", len(footprints))

print(
    "Metadata and footprint counts match:",
    len(metadata_sorted) == len(footprints)
)

print("\nSentinel-2 discovery completed successfully.")

print("Raw directory:", RAW_DIR)

print("Staging directory:", STAGING_DIR)
