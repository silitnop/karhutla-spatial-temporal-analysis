
from pathlib import Path

import geopandas as gpd
import pandas as pd


# ============================================================
# CONFIGURATION
# ============================================================

ROOT_DIR = Path(__file__).resolve().parents[2]

HOTSPOT_PATH = (
    ROOT_DIR
    / "data/processed/firms/hotspots_kalimantan_september_2026.geojson"
)

FOOTPRINT_PATH = (
    ROOT_DIR
    / "data/staging/sentinel2/sentinel2_september_2026_footprints.geojson"
)

OUTPUT_DIR = ROOT_DIR / "data/staging/sentinel2"

OUTPUT_PATH = (
    OUTPUT_DIR
    / "sentinel2_september_2026_hotspot_overlap.csv"
)


# ============================================================
# LOAD DATA
# ============================================================

print("=" * 60)
print("SENTINEL-2 HOTSPOT SPATIAL VALIDATION")
print("=" * 60)

hotspots = gpd.read_file(HOTSPOT_PATH)
footprints = gpd.read_file(FOOTPRINT_PATH)

print("\n===== DATA OVERVIEW =====")
print(f"Hotspot detections : {len(hotspots):,}")
print(f"Sentinel-2 products: {len(footprints):,}")
print(f"Hotspot CRS        : {hotspots.crs}")
print(f"Footprint CRS      : {footprints.crs}")


# ============================================================
# DATA VALIDATION
# ============================================================

if hotspots.crs is None or footprints.crs is None:
    raise ValueError("CRS information is missing.")

if hotspots.crs != footprints.crs:
    footprints = footprints.to_crs(hotspots.crs)

if not hotspots.geometry.is_valid.all():
    raise ValueError("Invalid hotspot geometries detected.")

if not footprints.geometry.is_valid.all():
    raise ValueError("Invalid Sentinel-2 footprint geometries detected.")

if hotspots.geometry.is_empty.any():
    raise ValueError("Empty hotspot geometries detected.")

if footprints.geometry.is_empty.any():
    raise ValueError("Empty footprint geometries detected.")

print("\nGeometry validation: PASSED")


# ============================================================
# SPATIAL JOIN
# ============================================================

print("\n===== SPATIAL INTERSECTION =====")


print("\n===== SPATIAL INTERSECTION =====")

footprint_columns = [
    "product_id",
    "datetime",
    "cloud_cover",
    "mgrs_tile",
    "platform",
    "geometry",
]

matches = gpd.sjoin(
    hotspots[["geometry"]],
    footprints[footprint_columns],
    how="inner",
    predicate="within",
)

print(f"Total hotspot-product matches: {len(matches):,}")

covered_hotspots = matches.index.nunique()
uncovered_hotspots = len(hotspots) - covered_hotspots

coverage_percentage = (
    covered_hotspots / len(hotspots) * 100
    if len(hotspots) > 0
    else 0
)

print(f"Hotspots covered  : {covered_hotspots:,}")
print(f"Hotspots uncovered: {uncovered_hotspots:,}")
print(f"Coverage          : {coverage_percentage:.2f}%")



# ============================================================
# AGGREGATE BY SENTINEL-2 PRODUCT
# ============================================================

print("\n===== AGGREGATE PRODUCT OVERLAP =====")

product_counts = (
    matches.groupby("product_id")
    .size()
    .rename("hotspot_detection_count")
)

result = footprints.drop(columns="geometry").copy()

result = result.merge(
    product_counts,
    on="product_id",
    how="left",
)

result["hotspot_detection_count"] = (
    result["hotspot_detection_count"]
    .fillna(0)
    .astype(int)
)

result["hotspot_coverage_pct"] = (
    result["hotspot_detection_count"]
    / len(hotspots)
    * 100
)

result = result.sort_values(
    by=["hotspot_detection_count", "cloud_cover"],
    ascending=[False, True],
)

# Rank is only based on hotspot overlap and product cloud cover.
result["priority_rank"] = (
    result["hotspot_detection_count"]
    .rank(method="dense", ascending=False)
    .astype(int)
)

# ============================================================
# SAVE OUTPUT
# ============================================================

OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

result.to_csv(OUTPUT_PATH, index=False)

print("\n===== OUTPUT =====")
print(f"Saved: {OUTPUT_PATH}")
print(f"Products evaluated: {len(result)}")

print("\n===== TOP 15 PRODUCTS =====")

print(
    result[
        [
            "product_id",
            "mgrs_tile",
            "datetime",
            "cloud_cover",
            "hotspot_detection_count",
            "priority_rank",
        ]
    ]
    .head(15)
    .to_string(index=False)
)

print("\n===== FINAL VALIDATION =====")
print(f"Output exists: {OUTPUT_PATH.exists()}")
print(f"Output rows  : {len(result)}")
print(
    "Products with hotspot overlap:",
    (result["hotspot_detection_count"] > 0).sum(),
)

print("\nSpatial validation completed successfully.")
