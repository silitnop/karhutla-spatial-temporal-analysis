# Data Analytics Notes
## Karhutla Spatial-Temporal Analysis

### 1. Overview

This document provides technical notes and data preparation information for the Data Analytics team working on the Karhutla Spatial-Temporal Analysis project.

The purpose of this handover is to explain the available datasets, database structure, data relationships, processing outputs, and known limitations before conducting exploratory data analysis, spatial-temporal analysis, clustering, and fire severity prediction.

The Data Engineering team has prepared the data ingestion, preprocessing, validation, and database infrastructure. The Data Analytics team is responsible for conducting the analytical workflows using the prepared datasets.

### 2. Analysis Scope

| Component | Description |
|---|---|
| Project Focus | Spatial-temporal analysis of fire activity in peatland ecosystems |
| Study Area | Five provinces in Kalimantan |
| Analysis Period | September 1–30, 2026 |
| Main Fire Data | NASA FIRMS active fire detections |
| Climate Data | CHIRPS daily precipitation |
| Spatial Reference | EPSG:4326 |
| Database | PostgreSQL 18.6 with PostGIS 3.7.0 |

The five study provinces are:

1. Kalimantan Barat
2. Kalimantan Selatan
3. Kalimantan Tengah
4. Kalimantan Timur
5. Kalimantan Utara

### 3. Available Datasets

The following datasets have been prepared for downstream analysis.

| Dataset | Prepared Data | Storage Location |
|---|---|---|
| FIRMS | Active fire hotspot detections | `02_Datasets/firms/` |
| CHIRPS | Daily precipitation GeoTIFF files | `02_Datasets/chirps/daily/` |
| Sentinel-2 | Product metadata and spatial footprints | `02_Datasets/sentinel2/` |
| Peatland | Cleaned peatland spatial features | `02_Datasets/peatland/` |
| Boundaries | Five provincial administrative boundaries | `02_Datasets/boundaries/` |

#### 3.1 FIRMS Active Fire Detections

Source: NASA Fire Information for Resource Management System (FIRMS).

Prepared dataset:

- `hotspots_kalimantan_september_2026.csv`
- `hotspots_kalimantan_september_2026.geojson`
- `hotspots_outside_study_area_september_2026.csv`

Data summary:

| Metric | Records |
|---|---:|
| Raw FIRMS records (September–October 2026) | 210,915 |
| September 2026 records | 115,739 |
| September records matched to the five study provinces | 115,137 |
| September records not matched to the study provinces | 602 |

The main analytical dataset contains 115,137 hotspot records for September 2026.

Relevant attributes include:

- `latitude` and `longitude`: geographic coordinates.
- `acq_date`: acquisition date.
- `acq_time`: acquisition time in integer HHMM-like format.
- `brightness`: satellite-measured brightness information.
- `frp`: Fire Radiative Power.
- `confidence`: detection confidence category.
- `satellite` and `instrument`: satellite and instrument information.
- `province_id`: matched province identifier.
- `geom`: PostGIS point geometry.

**Important considerations:**

- FIRMS records represent satellite-based active fire detections, not confirmed individual fire incidents.
- Multiple detections may be associated with the same fire event.
- Hotspot counts should not automatically be interpreted as burned area or fire severity.
- Confirm the source documentation's time-zone convention before converting `acq_time` into local time.
- The 602 unmatched records are retained separately and are not included in the main database hotspot table. An unmatched record should not automatically be interpreted as being outside Indonesia.

#### 3.2 CHIRPS Precipitation Data

Source: Climate Hazards Group InfraRed Precipitation with Station Data (CHIRPS).

Prepared data:

- 30 daily GeoTIFF raster files.
- Coverage: September 1–30, 2026.
- Coordinate Reference System: EPSG:4326.
- Approximate spatial resolution: 0.05 degrees.
- Raster dimensions: 210 × 188 pixels.
- Single-band raster.

Storage location:

`02_Datasets/chirps/daily/`

The database table `karhutla.chirps_raster_metadata` contains metadata and file paths for the daily raster files. The raster pixels remain in the external GeoTIFF files.

**Important considerations:**

- Access the actual raster pixels using Rasterio or GDAL.
- Check the source product documentation for the exact precipitation units and temporal interpretation before performing calculations.
- Handle NoData values (`-9999`) appropriately.
- Ensure raster and vector datasets use compatible coordinate reference systems during spatial analysis.
- Database metadata does not replace the original raster files.

#### 3.3 Sentinel-2 Product Metadata

Prepared dataset:

- `sentinel2_september_2026_footprints.geojson`
- `sentinel2_september_2026_metadata.csv`
- `sentinel2_september_2026_tile_summary.csv`
- `sentinel2_september_2026_hotspot_overlap.csv`
- `sentinel2_september_2026_top3_candidates_per_tile.csv`

The database table `karhutla.sentinel2_products` contains 214 product metadata records and their spatial footprints.

Relevant attributes include:

- `product_id`: Sentinel-2 product identifier.
- `acquisition_datetime`: acquisition timestamp.
- `cloud_cover`: product-level cloud cover percentage.
- `mgrs_tile`: MGRS tile identifier.
- `platform`: satellite platform.
- `instruments`: instrument information.
- `processing_level`: processing level.
- `collection`: product collection.
- `geom`: product footprint geometry.

**Important considerations:**

- The prepared Sentinel-2 data consists of metadata and spatial footprints, not downloaded satellite image pixels.
- Product-level cloud cover does not represent cloud coverage at a specific hotspot location.
- A hotspot may overlap multiple Sentinel-2 product footprints.
- Hotspot overlap percentages across different products are not mutually exclusive and may sum to more than 100%.
- The top-three candidate file is available, but its generating process or script provenance has not yet been verified. Confirm its methodology before using it as an analytical input.

Actual satellite imagery must be acquired separately if pixel-level spectral analysis or burned-area assessment is required.

#### 3.4 Peatland Spatial Data

Prepared dataset:

- `peatland_kalimantan_clean.geojson`
- `peatland_province_relationship.csv`

Database table:

`karhutla.dim_peatlands`

Data summary:

| Metric | Value |
|---|---:|
| Total peatland features | 350 |
| Features classified as gambut | 348 |
| Features with unknown classification | 2 |

Geometry type: MultiPolygon  
Coordinate Reference System: EPSG:4326

**Important considerations:**

- The peatland table does not have a direct foreign key to the province table.
- Use spatial relationships or the separately prepared province relationship dataset when linking peatlands to provinces.
- Check the source meaning of peatland attributes before assigning analytical interpretations.
- The units and calculation method of the original `shape_length` and `shape_area` attributes have not been independently verified.

#### 3.5 Provincial Boundaries

Prepared dataset:

`kalimantan_provinces.geojson`

Database table:

`karhutla.dim_provinces`

The dataset contains five provincial administrative boundaries.

Geometry type: MultiPolygon  
Coordinate Reference System: EPSG:4326

This dataset can be used for spatial filtering, geographic aggregation, and map visualization.

### 4. Database Access

The central analytical database is:

| Parameter | Value |
|---|---|
| Database | `karhutla_db` |
| Schema | `karhutla` |
| DBMS | PostgreSQL 18.6 |
| Spatial Extension | PostGIS 3.7.0 |
| Host | `localhost` for local installation |
| Port | `5432` by default |

Refer to `database_access_guide.md` for database restoration, connection instructions, and example SQL queries.

### 5. Database Table Overview

The database contains five main tables.

| Table | Records | Purpose |
|---|---:|---|
| `karhutla.dim_provinces` | 5 | Provincial boundaries |
| `karhutla.dim_peatlands` | 350 | Peatland spatial features |
| `karhutla.fact_hotspots` | 115,137 | FIRMS active fire detections |
| `karhutla.sentinel2_products` | 214 | Sentinel-2 metadata and footprints |
| `karhutla.chirps_raster_metadata` | 30 | CHIRPS raster metadata |

Total: 115,736 records.

### 6. Dataset Relationships and Integration

The following relationships can be used as a starting point for analytical integration.

| Dataset A | Dataset B | Relationship | Suggested Use |
|---|---|---|---|
| Hotspots | Provinces | `province_id` | Provincial hotspot aggregation |
| Hotspots | Peatlands | Spatial intersection or containment | Hotspot distribution within peatland areas |
| Hotspots | Sentinel-2 | Spatial footprint overlap | Identifying candidate satellite products |
| Hotspots | CHIRPS | Spatial and temporal matching | Exploring precipitation and fire activity |
| Peatlands | Provinces | Spatial relationship dataset | Peatland distribution by province |

**Important:**

- `fact_hotspots.province_id` references `dim_provinces.province_id`.
- `dim_peatlands` does not have a direct province foreign key.
- CHIRPS raster pixels are stored outside PostgreSQL.
- Sentinel-2 metadata and footprints do not provide spectral pixel values.
- Spatial joins should use compatible coordinate reference systems and appropriate spatial predicates.

### 7. Suggested Analytical Workflow

The following workflow is a suggested starting point for the Data Analytics team. The analytical methods and final decisions remain the responsibility of the Data Analytics team.

1. **Data Familiarization**
   - Inspect database tables, columns, data types, and record counts.
   - Review the data dictionary and source documentation.
   - Identify missing values, duplicates, and potential inconsistencies.

2. **Exploratory Data Analysis**
   - Examine hotspot distributions by date and province.
   - Explore FIRMS attributes such as brightness, FRP, and confidence.
   - Investigate daily precipitation patterns from CHIRPS.

3. **Spatial Analysis**
   - Examine hotspot distributions across provincial boundaries.
   - Investigate hotspot relationships with peatland areas.
   - Explore Sentinel-2 product footprint coverage.

4. **Temporal Analysis**
   - Examine daily hotspot activity throughout September 2026.
   - Explore temporal patterns in precipitation and hotspot detections.
   - Consider appropriate time alignment between datasets.

5. **Clustering**
   - Evaluate suitable spatial or spatiotemporal clustering methods.
   - Document selected parameters and assumptions.
   - Assess the stability and interpretation of identified clusters.

6. **Fire Severity Prediction**
   - First identify whether suitable ground-truth fire severity labels or burned-area measurements are available.
   - Assess whether the available features and labels are sufficient for supervised modelling.
   - Avoid treating FIRMS hotspot detections or FRP values alone as confirmed fire severity labels.

7. **Evaluation and Visualization**
   - Evaluate analytical results using appropriate metrics.
   - Document limitations and interpretation.
   - Prepare maps, charts, and dashboard-ready outputs.

### 8. Data Limitations and Recommendations

The following limitations should be considered throughout the analytical process.

| Limitation | Recommendation |
|---|---|
| FIRMS detects active fire signals rather than measuring burned area | Avoid interpreting hotspot counts as burned area |
| Multiple hotspot detections may represent related fire activity | Consider the possibility of repeated detections |
| FIRMS acquisition time requires time-zone interpretation | Verify source documentation before time conversion |
| Sentinel-2 imagery pixels have not been downloaded | Acquire imagery separately for spectral analysis |
| Sentinel-2 cloud cover is product-level metadata | Do not treat it as local pixel-level cloud coverage |
| CHIRPS pixels are stored externally | Maintain access to the shared GeoTIFF directory |
| Peatland-province relationships are not stored as a direct foreign key | Use the prepared relationship dataset or spatial analysis |
| Two peatland features have unknown classification | Review their treatment before category-based analysis |
| FIRMS records unmatched to the study provinces are excluded from the main table | Consider them separately if the study scope requires further investigation |
| Ground-truth fire severity labels have not been established | Verify label availability before supervised severity prediction |

### 9. Shared Resources

All prepared resources are available in the shared Google Drive folder:

`Karhutla Project - Shared Resources/`

Relevant directories:

| Directory | Contents |
|---|---|
| `01_Database/` | Database backup, schema, and database documentation |
| `02_Datasets/` | Prepared datasets for analysis |
| `03_Documentation/` | Data dictionary, data sources, and engineering progress |
| `04_Analysis_Handover/` | Database access guide and analytics notes |
| `05_Project_References/` | Project proposal and methodology |

The Data Analytics team should use the prepared datasets in the shared directory as the starting point for analysis.

### 10. Related Documentation

For further technical details, refer to:

- `04_Analysis_Handover/database_access_guide.md`
- `03_Documentation/data_dictionary.xlsx`
- `03_Documentation/data_sources.md`
- `03_Documentation/data_engineering_progress.md`
- `05_Project_References/project_proposal.pdf`
- `05_Project_References/project_methodology.pdf`

---

**Prepared by:** Data Engineering Team  
**For:** Data Analytics Team  
**Project:** Karhutla Spatial-Temporal Analysis  
**Last Updated:** November 22, 2026