# Database Documentation

This directory contains database-related resources for the Karhutla Spatial-Temporal Analysis project, including database backups and SQL schema definitions.

The project uses PostgreSQL and PostGIS to store and manage processed geospatial datasets used for spatial and temporal analysis of forest and land fires across five provinces in Kalimantan, Indonesia.

## Directory Structure

```text
database/
├── schema/
│   └── 01_create_schema.sql
├── backup/
│   └── karhutla_db.backup
└── README.md
```

### 1. Schema

Contains SQL scripts defining the database structure, including tables, primary keys, foreign keys, constraints, geometry columns, and spatial indexes.

### 2. Backup

Contains database backup files used to preserve the project's database and support database restoration.

The backup is created using PostgreSQL's custom backup format and can be restored using `pg_restore`.

## Database Technology

| Component | Technology |
|---|---|
| Database Management System | PostgreSQL 18 |
| Geospatial Extension | PostGIS |
| Query Language | SQL |
| Database Client | DBeaver |
| Python Integration | SQLAlchemy / Psycopg |

## Database Overview

The database contains five main tables:

| Table | Description |
|---|---|
| `dim_provinces` | Provincial boundaries of the study area |
| `dim_peatlands` | Peatland spatial data |
| `fact_hotspots` | FIRMS hotspot detections |
| `sentinel2_products` | Sentinel-2 product metadata and footprints |
| `chirps_raster_metadata` | Metadata and file references for CHIRPS daily rainfall rasters |

The database is intended to provide structured and accessible data for the Data Analytics team.

For connection details, database access instructions, table information, and sample queries, refer to `analysis_handover/database_access_guide.md` and the project's data dictionary.
