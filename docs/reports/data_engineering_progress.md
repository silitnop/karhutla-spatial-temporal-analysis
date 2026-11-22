# Data Engineering Progress Report

**Project:** Karhutla Spatial-Temporal Analysis  
**Role:** Data Engineering  
**Report Date:** November 22, 2026  
**Overall Status:** Core Database Implementation and Validation Completed; Final Handover in Progress

---

## 1. Overview

The Data Engineering phase focuses on collecting, preparing, transforming, validating, and integrating datasets required for the Karhutla Spatial-Temporal Analysis project.

The primary objective is to establish a centralized PostgreSQL database with PostGIS support, providing structured spatial and temporal data for subsequent analytical activities.

The database is designed to support the Data Analytics phase, including spatial analysis, hotspot clustering, temporal analysis, and data visualization.

In addition to the centralized database, processed datasets are maintained in the project repository to support independent access and analysis.

## 2. Data Sources and Ingestion Results

The following datasets have been collected, processed, and integrated into the database:

| Dataset | Description | Records |
|---|---|---:|
| Province Boundaries | Administrative boundaries of five Kalimantan provinces | 5 |
| Peatland | Peatland polygon features across Kalimantan | 350 |
| FIRMS Hotspots | Satellite-based active fire detections during September 2026 | 115,137 |
| Sentinel-2 | Satellite product metadata and spatial footprints | 214 |
| CHIRPS | Daily raster metadata for September 2026 | 30 |
| **Total** | | **115,736** |

### 2.1 Dataset Notes

- **FIRMS:** Contains satellite-based active fire detections, not confirmed burned-area measurements or fire severity labels.
- **Sentinel-2:** Currently contains product metadata and spatial footprints. The actual satellite imagery has not yet been downloaded.
- **CHIRPS:** Contains 30 daily GeoTIFF raster files. Raster pixel values remain stored in GeoTIFF files, while PostgreSQL stores their metadata and file references.
- **Peatland:** Contains 350 polygon features. The geometries were standardized for database storage and were not clipped to provincial boundaries.
- **FIRMS filtering:** A total of 115,137 September 2026 detections were matched to the five study provinces and loaded into the main database. An additional 602 unmatched records were retained separately for reference.

## 3. Data Engineering Activities

### 3.1 Data Ingestion

The following Python ingestion scripts have been implemented:

| Script | Purpose |
|---|---|
| `get_boundaries.py` | Retrieves administrative boundary data |
| `get_peatland.py` | Retrieves peatland data |
| `get_firms.py` | Retrieves FIRMS hotspot data |
| `get_chirps.py` | Retrieves daily CHIRPS raster data |
| `get_sentinel12.py` | Retrieves Sentinel-2 product metadata |

The collected datasets are organized into raw, staging, and processed directories to separate source data from intermediate and prepared outputs.

### 3.2 Data Transformation

The following data preparation and transformation activities have been performed:

- Standardized administrative boundary data for the five Kalimantan provinces.
- Cleaned and prepared peatland polygon attributes and geometries.
- Filtered FIRMS detections by the September 2026 analysis period and study area.
- Separated unmatched FIRMS records from the main study-area dataset.
- Prepared 30 daily CHIRPS raster datasets for September 2026.
- Processed Sentinel-2 product metadata and spatial footprints.
- Standardized spatial reference systems to EPSG:4326.
- Prepared peatland-to-province spatial relationship data.

Core data transformation activities have been completed. Further reproducibility checks and documentation remain part of the finalization process.

### 3.3 Database Implementation

The centralized database was implemented using:

- PostgreSQL 18.6
- PostGIS 3.7.0
- Python
- GeoPandas
- Rasterio
- Psycopg2

**Database Name:** `karhutla_db`  
**Schema Name:** `karhutla`

The database contains five primary tables:

| Table | Description | Records |
|---|---|---:|
| `dim_provinces` | Stores Kalimantan provincial boundaries | 5 |
| `dim_peatlands` | Stores peatland polygon information | 350 |
| `fact_hotspots` | Stores FIRMS hotspot detections | 115,137 |
| `sentinel2_products` | Stores Sentinel-2 product metadata and footprints | 214 |
| `chirps_raster_metadata` | Stores CHIRPS raster metadata and file references | 30 |

**Total database records: 115,736**

The database uses a structured schema to maintain relationships between spatial dimensions and hotspot observations.

### 3.4 Database Optimization

The database includes the following integrity and performance features:

- Primary key constraints.
- Foreign key relationships.
- Unique constraints.
- Check constraints.
- B-tree indexes for frequently queried attributes.
- GiST spatial indexes for geometry columns.

The `fact_hotspots` table references `dim_provinces` through `province_id`.

Spatial indexes are implemented on all four geometry tables to support spatial queries and improve the performance of location-based operations.

## 4. Data Validation Results

Several validation procedures have been performed after database ingestion.

| Validation | Result | Status |
|---|---|---|
| Record count validation | All five tables match expected counts | Passed |
| Hotspot province relationship | 115,137 valid province references | Passed |
| Invalid province references | 0 | Passed |
| Invalid geometries | 0 across 115,706 spatial records | Passed |
| Spatial reference validation | EPSG:4326 across all spatial tables | Passed |
| Spatial index verification | GiST indexes found on all four geometry tables | Passed |
| Peatland feature validation | 350 valid geometries | Passed |

All five database tables have been successfully populated and passed the recorded validation checks.

## 5. Database Backup

A PostgreSQL custom-format backup has been generated.

**File:** `karhutla_db.backup`  
**Format:** PostgreSQL Custom Format (`pg_dump -F c`)  
**Location:** `database/backup/karhutla_db.backup`  
**Size:** Approximately 22.74 MiB

The backup archive has been inspected using `pg_restore -l`.

The archive contains:

- The `karhutla` schema.
- PostGIS extension definition.
- All five database tables.
- Table data.
- Primary and foreign key constraints.
- Index definitions.
- Sequence definitions and values.
- Spatial reference system data.

### 5.1 Backup Restore Testing

A separate restore test was successfully performed using a temporary database named `karhutla_restore_test`.

All five tables were successfully restored, and their record counts matched the original database:

| Table | Restored Records |
|---|---:|
| `dim_provinces` | 5 |
| `dim_peatlands` | 350 |
| `fact_hotspots` | 115,137 |
| `sentinel2_products` | 214 |
| `chirps_raster_metadata` | 30 |
| **Total** | **115,736** |

The PostGIS extension was also verified successfully using `PostGIS_Full_Version()`, confirming that PostGIS 3.7.0 was available in the restored database.

The restore test confirmed that the backup archive can successfully reconstruct the database structure, data, constraints, indexes, and PostGIS extension.

**Restore Test Result:** Successful.

---

## 6. Current Progress Status

| Activity | Status |
|---|---|
| Dataset collection | Completed |
| Data ingestion scripts | Implemented |
| Core data transformation | Completed |
| Database schema implementation | Completed |
| Dataset ingestion into PostgreSQL | Completed |
| Database integrity validation | Completed |
| Spatial validation | Completed |
| Database indexing and optimization | Completed |
| Database backup creation | Completed |
| Backup archive inspection | Completed |
| Backup restore testing | Completed |
| Database documentation | In progress |
| Data dictionary and source documentation | Pending |
| Data Analytics handover preparation | In progress |

---

## 7. Pending Activities

The remaining Data Engineering activities include:

1. Complete database documentation and data dictionary references.
2. Verify CHIRPS raster file availability using the file paths stored in PostgreSQL.
3. Prepare database access and usage instructions for the Data Analytics team.
4. Organize processed datasets and relevant Sentinel-2 metadata for handover.
5. Finalize the Data Engineering handover documentation.

---

## 9. Conclusion

The core Data Engineering implementation for the Karhutla Spatial-Temporal Analysis project has been completed.

The project has successfully established a PostgreSQL database with PostGIS support, integrated five datasets, implemented database constraints and indexes, and performed data integrity and spatial validation.

Database backup creation and restoration have also been successfully verified through a separate restore test, including validation of all five table record counts and PostGIS availability.

The current focus is on documentation completion, dataset organization, and preparing the required resources for the Data Analytics team.

**Report Status:** Core database implementation, ingestion, validation, backup creation, and restore testing completed. Final handover remains in progress pending documentation and handover preparation.