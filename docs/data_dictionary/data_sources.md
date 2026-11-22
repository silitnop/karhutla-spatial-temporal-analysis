# Data Sources

## 1. Overview

This document describes the data sources used in the Karhutla Spatial-Temporal Analysis project. It provides information about each dataset, including its provider, data format, temporal coverage, storage location, and purpose within the data engineering workflow.

The project uses satellite-based fire detections, climate data, administrative boundaries, peatland data, and Sentinel-2 product metadata to support spatial and temporal analysis of forest and land fires in Kalimantan.

## 2. Dataset Inventory

| Dataset | Source / Provider | Format | Temporal Coverage | Storage Location |
|---|---|---|---|---|
| FIRMS Active Fire | NASA FIRMS | CSV | September 1–October 31, 2026 (raw acquisition); September 1–30, 2026 (study period) | `data/raw/firms/` |
| CHIRPS Precipitation | Climate Hazards Center | GeoTIFF | September 1–30, 2026 | `data/raw/chirps/` |
| Provincial Boundaries | Badan Informasi Geospasial (BIG) | GeoJSON | Static reference data | `data/raw/boundaries/` |
| Peatland Boundaries | World Resources Institute (WRI), accessed through BNPB GIS service | GeoJSON | Static reference data | `data/raw/peatland/` |
| Sentinel-2 Product Metadata | Copernicus Data Space Ecosystem | GeoJSON | September 2026 search results | `data/raw/sentinel2/` |

## 3. Dataset Descriptions

### 3.1 FIRMS Active Fire

- **Provider:** NASA Fire Information for Resource Management System (FIRMS)
- **Format:** CSV
- **Content:** Satellite-based active fire and thermal anomaly detections.
- **Raw Acquisition Period:** September 1–October 31, 2026.
- **Study Period:** September 1–30, 2026.
- **Purpose:** Provides hotspot locations and detection attributes for spatial and temporal analysis.
- **Acquisition Method:** An existing FIRMS CSV source file is used as the raw input. The ingestion script performs source file verification and inspection rather than downloading data directly from NASA.
- **Ingestion Script:** `data_engineering/ingestion/get_firms.py`
- **Raw Files:**
  - `data/raw/firms/fire_nrt_SV-C2_852079.csv`
  - `data/raw/firms/Readme.txt`

**Processed Outputs:**

- `data/processed/firms/hotspots_kalimantan_september_2026.csv`
- `data/processed/firms/hotspots_kalimantan_september_2026.geojson`
- `data/processed/firms/hotspots_outside_study_area_september_2026.csv`

**Important Note:** FIRMS detections represent active fire or thermal anomalies. They should not be interpreted directly as burned area or fire severity measurements.

### 3.2 CHIRPS Precipitation

- **Provider:** Climate Hazards Center, University of California, Santa Barbara (UCSB)
- **Product:** CHIRPS v3.0 Daily Final Satellite
- **Format:** GeoTIFF
- **Content:** Daily gridded precipitation estimates.
- **Study Period:** September 1–30, 2026.
- **Purpose:** Provides daily precipitation data for environmental and temporal analysis.
- **Acquisition Method:** Daily raster files are downloaded directly from the Climate Hazards Center data repository using HTTP requests.
- **Source Directory:** `https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/sat/2026/`
- **Ingestion Script:** `data_engineering/ingestion/get_chirps.py`
- **Raw Location:** `data/raw/chirps/`
- **Processed Location:** `data/processed/chirps/daily/`

**Processing and Ingestion:**

1. Generates daily filenames for September 1–30, 2026.
2. Checks whether each output file already exists and has a non-zero size.
3. Downloads missing files using HTTP streaming.
4. Removes incomplete output files when a download request fails.

**Important Notes:**

- CHIRPS provides gridded precipitation estimates rather than direct rainfall station measurements.
- Raw and processed raster files are maintained separately.
- PostgreSQL stores raster metadata and file paths; raster pixel values remain in the GeoTIFF files.

### 3.3 Provincial Boundaries

- **Provider:** Badan Informasi Geospasial (BIG)
- **Service:** Rupa Bumi Indonesia (RBI) Administrative Boundaries
- **API Type:** ArcGIS REST API
- **Format:** GeoJSON
- **Source Layer:** `BATASWILAYAH/BATAS_WILAYAH/MapServer/12`
- **Content:** Administrative boundaries of the five Kalimantan provinces included in the study.
- **Acquisition Method:** Retrieved through the BIG geospatial service using a province-name filter.
- **Coordinate Reference System:** EPSG:4326
- **Purpose:** Defines the geographical study area and supports spatial filtering and province-level assignment.
- **Raw Location:** `data/raw/boundaries/kalimantan_provinces.geojson`
- **Processed Location:** `data/processed/boundaries/kalimantan_provinces.geojson`

### 3.4 Peatland Boundaries

- **Original Dataset Attribution:** World Resources Institute (WRI)
- **Service Provider:** Badan Nasional Penanggulangan Bencana (BNPB)
- **GIS Service:** InAWARE / Global Forest Watch 2
- **Layer Name:** `Indonesia_peat_lands`
- **API Type:** ArcGIS REST API
- **Source Layer:** `InAWARE/Global_forest_watch2/MapServer/3`
- **Format:** GeoJSON
- **Geometry Type:** Polygon
- **Content:** Digital spatial representation of peatland areas in Indonesia.
- **Acquisition Method:** Retrieved through an ArcGIS spatial query using a geographical bounding box covering the Kalimantan region.
- **Bounding Box:** 108°E–119°E, 5°S–8°N
- **Coordinate Reference System:** EPSG:4326
- **Purpose:** Provides peatland spatial features for analyzing the spatial relationship between peatland areas and active fire detections.
- **Raw Location:** `data/raw/peatland/peatland_kalimantan_bbox.geojson`
- **Processed Location:** `data/processed/peatland/`
- **Processing Notebook:** `data_engineering/transformation/peatland_cleaning.ipynb`

**Data Processing:**

1. Inspected dataset structure, attributes, missing values, duplicate records, and geometry validity.
2. Normalized the `layer_revi` attribute by removing surrounding whitespace and replacing blank categories with `unknown`.
3. Standardized the peatland CRS to match the provincial boundary dataset.
4. Performed a spatial join using the `intersects` predicate to identify peatland-province relationships.
5. Generated a separate CSV containing unique peatland-province relationships.
6. Exported the cleaned peatland GeoJSON and relationship CSV.
7. Re-read the exported files to validate the output.

**Output Files:**

- `peatland_kalimantan_clean.geojson`
- `peatland_province_relationship.csv`

**Important Notes:**

- The BNPB GIS service is the endpoint used for data retrieval, while the layer description attributes the original dataset to World Resources Institute (WRI).
- The service metadata specifies a maximum record count of 1,000. The current query returned 350 features, but complete source coverage has not been independently verified.
- The bounding-box query does not guarantee that every returned feature belongs to the five study provinces.
- Geometry validity is inspected during processing, but invalid geometries are not automatically repaired.
- A peatland polygon may intersect multiple provinces. Therefore, the relationship table can contain multiple province records for one polygon.

### 3.5 Sentinel-2 Product Metadata

- **Provider:** Copernicus Data Space Ecosystem
- **Catalog:** SpatioTemporal Asset Catalog (STAC)
- **STAC API:** `https://stac.dataspace.copernicus.eu/v1`
- **Collection:** `sentinel-2-l2a`
- **Format:** GeoJSON and CSV
- **Study Period:** September 1–30, 2026 (UTC)
- **Maximum Cloud Cover:** 30%
- **Content:** Sentinel-2 Level-2A product metadata and spatial footprints.
- **Purpose:** Provides satellite product metadata, acquisition timestamps, cloud cover information, and spatial footprints for potential imagery selection.
- **Acquisition Method:** Products are discovered through the Copernicus STAC API using the study area's bounding box, acquisition date range, and cloud cover filter.
- **Spatial Filtering:** Product footprints are checked against the Kalimantan study area using the `intersects` predicate.
- **Ingestion Script:** `data_engineering/ingestion/get_sentinel12.py`
- **Spatial Validation Script:** `data_engineering/transformation/validate_sentinel2_hotspot_overlap.py`

**Raw Location:**

- `data/raw/sentinel2/sentinel2_september_2026_stac_search.geojson`

**Staging Outputs:**

- `data/staging/sentinel2/sentinel2_september_2026_footprints.geojson`
- `data/staging/sentinel2/sentinel2_september_2026_metadata.csv`
- `data/staging/sentinel2/sentinel2_september_2026_tile_summary.csv`
- `data/staging/sentinel2/sentinel2_september_2026_top3_candidates_per_tile.csv`
- `data/staging/sentinel2/sentinel2_september_2026_hotspot_overlap.csv`

**Processing and Ingestion:**

1. Loads and validates the five provincial boundary geometries.
2. Standardizes the study area to EPSG:4326.
3. Queries the Copernicus STAC API for Sentinel-2 Level-2A products.
4. Applies acquisition date and maximum cloud cover filters.
5. Handles paginated API responses and retries failed requests.
6. Filters products whose footprints intersect the study area.
7. Extracts product metadata, including product ID, acquisition datetime, cloud cover, MGRS tile, platform, instrument, and processing level.
8. Generates metadata summaries and spatial footprint outputs.
9. Compares FIRMS hotspot locations against Sentinel-2 product footprints using a spatial join with the `within` predicate.
10. Aggregates hotspot-product matches by product ID and calculates hotspot detection counts and relative coverage percentages.
11. Ranks products based on hotspot detection counts to support further product selection.

**Database Loading:**

- **Loading Script:** `data_engineering/database/scripts/load_sentinel12.py`
- **Target Table:** `karhutla.sentinel2_products`
- **Source:** `data/staging/sentinel2/sentinel2_september_2026_footprints.geojson`
- **Database:** PostgreSQL with PostGIS
- **Geometry Type:** Polygon
- **Target CRS:** EPSG:4326

The loading script validates source metadata, geometry validity, geometry type, CRS, duplicate product IDs, and cloud cover ranges before inserting records into PostgreSQL. Database records are validated after loading.

**Important Notes:**

- The raw STAC search response contains products returned by the bounding-box query. The staging outputs contain products filtered by actual intersection with the study area.
- The current database contains 214 Sentinel-2 product records.
- Cloud cover values represent product-level metadata, not local cloud conditions at individual hotspot locations.
- The hotspot overlap output counts spatial relationships between hotspot detections and product footprints. A hotspot may intersect multiple product footprints.
- `hotspot_coverage_pct` represents the proportion of all study-area hotspot detections associated with a product, not the percentage of geographic area covered by satellite imagery.
- Product priority ranking is based on hotspot detection counts, with cloud cover used for sorting.
- The current workflow retrieves metadata and footprints only. Actual satellite imagery pixels have not been downloaded.
- The `sentinel2_september_2026_top3_candidates_per_tile.csv` file exists in the staging directory, but its generating script or process has not yet been identified. Its provenance remains unverified.

## 4. Coordinate Reference System

The spatial datasets used in the current data engineering workflow are standardized to:

- **CRS:** EPSG:4326
- **Coordinate System:** WGS 84

Coordinate reference systems are checked and standardized where necessary before spatial operations, such as spatial joins and geographical filtering.

Non-spatial datasets, including CSV files containing attributes or metadata, do not have an independent coordinate reference system.

## 5. Data Availability and Limitations

- FIRMS data represents satellite-based active fire detections and thermal anomalies, not confirmed fire incidents or direct burned-area measurements.
- The raw FIRMS acquisition covers a broader period than the September 2026 study period. Only September records are used for the main study dataset.
- CHIRPS provides gridded precipitation estimates rather than direct rainfall station measurements.
- Provincial boundaries are retrieved from the BIG Rupa Bumi Indonesia geospatial service.
- Peatland data is attributed to World Resources Institute (WRI) based on the BNPB GIS layer description. The BNPB GIS service is used as the data access endpoint.
- The peatland API query returned 350 features. However, complete source coverage has not been independently verified.
- Peatland geometry validity is inspected during processing, but invalid geometries are not automatically repaired.
- Sentinel-2 records currently contain product metadata and spatial footprints only. Actual satellite imagery pixels have not been downloaded.
- Sentinel-2 cloud cover represents product-level metadata, not local cloud conditions for individual locations.
- CHIRPS raster files are stored externally as GeoTIFF files. PostgreSQL stores their metadata and file paths rather than the raster pixel values.
- Data availability, spatial coverage, and completeness depend on the respective providers and acquisition methods.

## 6. Data Storage Structure

The project separates datasets according to their processing stages:

| Directory | Description |
|---|---|
| `data/raw/` | Original datasets collected from external sources. |
| `data/staging/` | Intermediate data prepared for further processing. |
| `data/processed/` | Cleaned and transformed datasets. |
| `data/final/` | Final datasets prepared for downstream analytical use. |

---

*This document is maintained by the Data Engineering team and should be updated whenever a dataset source, acquisition period, or processing workflow changes.*