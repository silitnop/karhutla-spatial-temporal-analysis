
from pathlib import Path
import pandas as pd

# ==========================================
# CONFIGURATION
# ==========================================

RAW_DIR = Path("data/raw/firms")

SOURCE_FILE = RAW_DIR / "fire_nrt_SV-C2_852079.csv"
README_FILE = RAW_DIR / "Readme.txt"


# ==========================================
# INGESTION CHECK
# ==========================================

def main():
    print("NASA FIRMS DATA INGESTION")
    print("=" * 45)

    # Check source directory
    if not RAW_DIR.exists():
        print("[ERROR] FIRMS directory not found.")
        return

    # Check source CSV
    if not SOURCE_FILE.exists():
        print("[ERROR] FIRMS CSV file not found.")
        return

    print("[SUCCESS] Source CSV found.")

    # Read source data
    try:
        df = pd.read_csv(SOURCE_FILE)

        print(f"Filename       : {SOURCE_FILE.name}")
        print(f"Total records  : {len(df):,}")
        print(f"Total columns  : {len(df.columns)}")
        print(f"File size      : {SOURCE_FILE.stat().st_size / (1024 * 1024):.2f} MB")

        print("\nAvailable columns:")
        print(list(df.columns))

    except Exception as error:
        print(f"[ERROR] Failed to read CSV: {error}")
        return

    # Check documentation
    if README_FILE.exists():
        print("\n[SUCCESS] Source documentation found.")
    else:
        print("\n[WARNING] Readme.txt not found.")

    print("\n" + "=" * 45)
    print("FIRMS INGESTION CHECK COMPLETED")


if __name__ == "__main__":
    main()
