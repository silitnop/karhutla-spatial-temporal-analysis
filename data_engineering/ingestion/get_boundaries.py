
import requests
import geopandas as gpd
from pathlib import Path

# BIG API
url = (
    "https://geoservices.big.go.id/rbi/rest/services/"
    "BATASWILAYAH/BATAS_WILAYAH/MapServer/12/query"
)

# Lima provinsi penelitian
provinces = [
    "Kalimantan Barat",
    "Kalimantan Selatan",
    "Kalimantan Tengah",
    "Kalimantan Timur",
    "Kalimantan Utara"
]

# Filter berdasarkan nama provinsi
where_clause = (
    "wadmpr IN ("
    + ", ".join(f"'{province}'" for province in provinces)
    + ")"
)

params = {
    "where": where_clause,
    "outFields": "*",
    "returnGeometry": "true",
    "outSR": 4326,
    "f": "geojson"
}

print("Mengambil data batas administrasi BIG...")

response = requests.get(url, params=params, timeout=60)
response.raise_for_status()

data = response.json()

if "error" in data:
    raise RuntimeError(data["error"])

# Konversi GeoJSON menjadi GeoDataFrame
gdf = gpd.GeoDataFrame.from_features(
    data["features"],
    crs="EPSG:4326"
)

# Validasi hasil
print("\nJumlah fitur:", len(gdf))
print("\nProvinsi ditemukan:")
print(gdf["wadmpr"].tolist())

# Simpan hasil
output_dir = Path("data/raw/boundaries")
output_dir.mkdir(parents=True, exist_ok=True)

output_file = output_dir / "kalimantan_provinces.geojson"

gdf.to_file(output_file, driver="GeoJSON")

print("\nData berhasil disimpan:", output_file)

