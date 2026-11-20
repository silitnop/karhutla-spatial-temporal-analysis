import geopandas as gpd
from pathlib import Path

# Load data hasil ingestion BIG
input_file = "data/raw/boundaries/kalimantan_provinces.geojson"

gdf = gpd.read_file(input_file)

# Rapikan nama provinsi
gdf["wadmpr"] = (
    gdf["wadmpr"]
    .str.strip()
    .replace({
        "KalimantanTengah": "Kalimantan Tengah"
    })
)

# Gabungkan polygon berdasarkan provinsi
provinces = gdf.dissolve(by="wadmpr")

# Reset index agar nama provinsi menjadi kolom
provinces = provinces[["geometry"]].reset_index()

# Validasi hasil
print("Jumlah provinsi:", len(provinces))
print("\nNama provinsi:")
print(provinces["wadmpr"].tolist())

print("\nGeometry valid:")
print(provinces.geometry.is_valid.all())

# Simpan hasil transformasi
output_file = Path(
    "data/processed/boundaries/kalimantan_provinces.geojson"
)

output_file.parent.mkdir(parents=True, exist_ok=True)

provinces.to_file(output_file, driver="GeoJSON")

print("\nData berhasil disimpan:", output_file)