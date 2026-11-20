
from pathlib import Path
import requests

# ==========================================
# CONFIGURATION
# ==========================================

BASE_URL = (
    "https://gis.bnpb.go.id/server/rest/services/"
    "InAWARE/Global_forest_watch2/MapServer/3/query"
)

RAW_DIR = Path("data/raw/peatland")
OUTPUT_FILE = RAW_DIR / "peatland_kalimantan_bbox.geojson"

BBOX = "108,-5,119,8"


# ==========================================
# INGESTION
# ==========================================

def main():
    RAW_DIR.mkdir(parents=True, exist_ok=True)

    print("BNPB PEATLAND DATA INGESTION")
    print("=" * 45)

    # Skip if source file already exists
    if OUTPUT_FILE.exists() and OUTPUT_FILE.stat().st_size > 0:
        print("[INFO] Source file already exists.")
        print(f"[INFO] File: {OUTPUT_FILE}")
        print("[INFO] Skipping download.")
        return

    params = {
        "where": "1=1",
        "geometry": BBOX,
        "geometryType": "esriGeometryEnvelope",
        "inSR": 4326,
        "spatialRel": "esriSpatialRelIntersects",
        "outFields": "*",
        "returnGeometry": "true",
        "outSR": 4326,
        "f": "geojson",
        "resultRecordCount": 1000
    }

    try:
        response = requests.get(
            BASE_URL,
            params=params,
            timeout=120
        )

        response.raise_for_status()

        data = response.json()

        if "error" in data:
            raise ValueError(data["error"])

        features = data.get("features", [])

        if not features:
            raise ValueError("No features returned from BNPB API.")

        OUTPUT_FILE.write_text(
            response.text,
            encoding="utf-8"
        )

        print("[SUCCESS] Peatland data retrieved.")
        print(f"Total features : {len(features)}")
        print(f"Output file    : {OUTPUT_FILE}")

    except (requests.RequestException, ValueError) as error:
        print(f"[ERROR] Ingestion failed: {error}")


if __name__ == "__main__":
    main()
