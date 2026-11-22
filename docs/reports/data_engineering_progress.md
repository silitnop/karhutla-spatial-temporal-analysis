# Data Engineering Progress Report

**Project:** Karhutla Spatial-Temporal Analysis  
**Role:** Data Engineering  
**Report Date:** November 22, 2026  
**Status:** Database Ingestion Completed

---

## 1. Overview

The Data Engineering phase focuses on collecting, preparing, validating, and integrating datasets required for the Karhutla Spatial-Temporal Analysis project.

The primary objective is to establish a centralized PostgreSQL database with PostGIS support, allowing the Data Analytics team to access structured spatial and temporal data for further analysis.

The database serves as the central data source for subsequent analytical activities, including spatial analysis, hotspot clustering, temporal analysis, and visualization.

## 2. Data Sources and Ingestion Results

The following datasets have been collected and processed:

| Dataset | Description | Records |
|---|---|---:|
| Province Boundaries | Administrative boundaries of five Kalimantan provinces | 5 |
| Peatland | Peatland polygon features across Kalimantan | 350 |
| FIRMS Hotspots | Satellite-based active fire detections during September 2026 | 115,137 |
| Sentinel-2 | Satellite product metadata and spatial footprints | 214 |
| CHIRPS | Daily raster metadata for September 2026 | 30 |
| **Total** | | **115,736** |

### Dataset Notes

- FIRMS data contains active fire hotspot detections, not confirmed burned-area measurements.
- Sentinel-2 data currently contains product metadata and spatial footprints. The actual satellite imagery has not yet been downloaded.
- CHIRPS raster pixels remain stored as GeoTIFF files. Only their metadata and file references are stored in PostgreSQL.

## 3. Data Engineering Activities

### 3.1 Data Ingestion

The following ingestion scripts have been implemented:

| Script | Purpose |
|---|---|
| `get_boundaries.py` | Collects administrative boundary data |
| `get_peatland.py` | Collects peatland data |
| `get_firms.py` | Retrieves FIRMS hotspot data |
| `get_chirps.py` | Retrieves daily CHIRPS raster data |
| `get_sentinel12.py` | Retrieves Sentinel-2 product metadata |

### 3.2 Data Transformation

Data preparation and transformation activities include:

- Cleaning and standardizing administrative boundary data.
- Preparing peatland polygon attributes and geometries.
- Filtering FIRMS hotspot detections within the study area.
- Preparing daily CHIRPS raster datasets.
- Processing Sentinel-2 metadata and spatial footprints.
- Standardizing spatial reference systems to EPSG:4326.

### 3.3 Database Implementation

The centralized database was implemented using:

- PostgreSQL 18.6
- PostGIS 3.7.0
- Python
- GeoPandas
- Rasterio
- Psycopg2

Database name: `karhutla_db`

Schema name: `karhutla`

The database contains five primary tables:

| Table | Description |
|---|---|
| `dim_provinces` | Stores Kalimantan provincial boundaries |
| `dim_peatlands` | Stores peatland polygon information |
| `fact_hotspots` | Stores FIRMS hotspot detections |
| `sentinel2_products` | Stores Sentinel-2 product metadata and footprints |
| `chirps_raster_metadata` | Stores CHIRPS raster metadata and file references |

### 3.4 Database Optimization

The database includes:

- Primary key constraints.
- Foreign key relationships.
- Unique constraints.
- Check constraints.
- B-tree indexes for frequently queried attributes.
- GiST spatial indexes for geometry columns.

The `fact_hotspots` table references `dim_provinces` through `province_id`.

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

All five database tables have been successfully populated and validated.

## 5. Database Backup

A PostgreSQL custom-format backup has been generated:

**File:** `karhutla_db.backup`

**Format:** Custom (`pg_dump -F c`)

The backup archive has been inspected using `pg_restore -l`.

The archive contains:

- The `karhutla` schema.
- PostGIS extension.
- All five database tables.
- Table data.
- Primary and foreign key constraints.
- Indexes.
- Sequence definitions and values.
- Spatial reference system data.

A separate database restore test has not yet been performed.

## 6. Current Progress Status

| Activity | Status |
|---|---|
| Dataset collection | Completed |
| Data transformation | Initial preparation completed |
| Database schema implementation | Completed |
| Dataset ingestion | Completed |
| Database integrity validation | Completed |
| Spatial validation | Completed |
| Database backup creation | Completed |
| Backup restore testing | Pending |
| Database documentation | In progress |
| Data handover to Data Analytics | Pending |

## 7. Pending Activities

The remaining Data Engineering activities include:

1. Perform a database restore test using a separate PostgreSQL database.
2. Complete database documentation and data dictionary references.
3. Verify the availability of CHIRPS raster files using their stored file paths.
4. Prepare database access and usage instructions for the Data Analytics team.
5. Finalize the Data Engineering handover.

## 8. Handover to Data Analytics

The Data Engineering team will provide the following resources to support the Data Analytics phase:

- PostgreSQL database backup.
- SQL schema definition.
- Python ingestion scripts.
- Processed datasets.
- Dataset documentation and data dictionary.
- Database structure and relationship documentation.

The Data Analytics team can use the centralized database as the primary source for analytical queries and subsequent processing.

CHIRPS GeoTIFF files must also be available to the team because the database stores their metadata and file references rather than the raster pixel data itself.

Sentinel-2 imagery acquisition and further image processing remain separate activities.

---

**Report Status:** Database ingestion and initial validation completed. Final handover is pending restore testing and documentation.