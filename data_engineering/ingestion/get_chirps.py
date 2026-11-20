
from pathlib import Path
import requests

# ==========================================
# CONFIGURATION
# ==========================================

BASE_URL = (
    "https://data.chc.ucsb.edu/products/"
    "CHIRPS/v3.0/daily/final/sat/2026/"
)

OUTPUT_DIR = Path("data/raw/chirps")

YEAR = 2026
MONTH = 9
DAYS = range(1, 31)


# ==========================================
# DOWNLOAD FUNCTION
# ==========================================

def download_file(url, output_path):
    try:
        response = requests.get(url, stream=True, timeout=60)
        response.raise_for_status()

        with open(output_path, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    file.write(chunk)

        print(f"[DOWNLOADED] {output_path.name}")

    except requests.RequestException as error:
        print(f"[FAILED] {output_path.name}: {error}")

        if output_path.exists():
            output_path.unlink()


# ==========================================
# MAIN PROCESS
# ==========================================

def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print("CHIRPS DATA INGESTION")
    print("=" * 40)

    for day in DAYS:
        filename = (
            f"chirps-v3.0.sat."
            f"{YEAR}.{MONTH:02d}.{day:02d}.tif"
        )

        output_path = OUTPUT_DIR / filename
        url = BASE_URL + filename

        if output_path.exists() and output_path.stat().st_size > 0:
            print(f"[SKIPPED] {filename} already exists")
            continue

        download_file(url, output_path)

    print("=" * 40)
    print("INGESTION PROCESS FINISHED")


if __name__ == "__main__":
    main()
