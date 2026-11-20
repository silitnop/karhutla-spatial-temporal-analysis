# Administrative Boundaries Data Dictionary

## 1. Dataset Overview

| Attribute | Description |
|---|---|
| Dataset Name | Kalimantan Provincial Administrative Boundaries |
| Data Source | Badan Informasi Geospasial (BIG) |
| Source Website | https://tanahair.indonesia.go.id/ |
| Data Format | GeoJSON |
| Geometry Type | MultiPolygon |
| Coordinate Reference System | EPSG:4326 |
| Administrative Level | Province |
| Number of Features | 5 |
| Study Area | Five provinces in Kalimantan, Indonesia |

## 2. Dataset Description

This dataset contains the provincial administrative boundaries of five provinces in Kalimantan, Indonesia.

The original BIG dataset consists of 56 administrative features representing regencies and cities. These features were grouped by province using a spatial dissolve operation to generate five provincial boundary geometries.

Each feature represents one province and contains a MultiPolygon geometry that defines its spatial extent.

## 3. Source Dataset

**Source file:**

`data/raw/boundaries/kalimantan_provinces.geojson`

| Attribute | Value |
|---|---|
| Total Features | 56 |
| Administrative Level | Regency / City |
| Source Geometry | Polygon / MultiPolygon (original source geometry types should be checked if needed) |
| Coordinate Reference System | EPSG:4326 |

## 4. Processed Dataset Structure

**Output file:**

`data/processed/boundaries/kalimantan_provinces.geojson`

| Column | Data Type | Description | Unit / Notes |
|---|---|---|---|
| wadmpr | String | Provincial administrative name | Province name |
| geometry | MultiPolygon | Provincial boundary geometry | EPSG:4326 |

### Province Coverage

| Province |
|---|
| Kalimantan Barat |
| Kalimantan Tengah |
| Kalimantan Selatan |
| Kalimantan Timur |
| Kalimantan Utara |

## 5. Spatial Processing

The raw administrative boundaries were transformed through the following steps:

1. Load the original BIG GeoJSON dataset.
2. Normalize province names in the `wadmpr` attribute.
3. Group administrative features based on `wadmpr`.
4. Apply the dissolve operation to combine regency and city geometries into provincial boundaries.
5. Retain the province name and merged geometry.
6. Export the processed dataset as GeoJSON.

The dissolve operation produces one MultiPolygon feature for each province.

## 6. Spatial Validation

The processed dataset was checked for:

| Validation | Result |
|---|---|
| Raw feature count | 56 |
| Processed feature count | 5 |
| Province coverage | 5 provinces |
| Geometry type | MultiPolygon |
| Geometry validity | All valid |
| Coordinate Reference System | EPSG:4326 |

### Approximate Area by Province

Area was calculated after projecting the geometries to EPSG:6933.

| Province | Approximate Area (km²) |
|---|---:|
| Kalimantan Barat | 147,018.06 |
| Kalimantan Selatan | 37,125.43 |
| Kalimantan Tengah | 153,430.36 |
| Kalimantan Timur | 126,951.76 |
| Kalimantan Utara | 69,900.89 |
| **Total** | **534,426.49** |

These values represent calculated geometry areas and should not be treated as official administrative area statistics.

## 7. Usage in the Project

The processed provincial boundaries serve as the primary spatial reference for:

- Filtering hotspot detections within the study area.
- Assigning hotspot records to their corresponding provinces.
- Cropping CHIRPS rainfall rasters to the study area.
- Identifying spatial relationships between peatland areas and provinces.
- Supporting downstream spatial analysis and data integration.

## 8. Important Notes

1. The raw dataset is retained unchanged in the `raw/` directory.
2. The processed dataset contains one merged geometry per province.
3. EPSG:4326 is used as the common geographic coordinate reference system for spatial integration.
4. Area calculations use EPSG:6933 rather than directly calculating area from geographic coordinates.
5. Provincial geometries are derived from the original BIG administrative boundary dataset.

## 9. References

- Badan Informasi Geospasial (BIG): https://tanahair.indonesia.go.id/