# Database Access Guide
## Karhutla Spatial-Temporal Analysis

### 1. Overview

This document provides instructions for accessing and using the PostgreSQL database prepared for the Karhutla Spatial-Temporal Analysis project.

The database serves as the central data source for downstream data analytics, including exploratory data analysis, spatial analysis, and temporal analysis.

### 2. Database Environment

| Component | Configuration |
|---|---|
| DBMS | PostgreSQL 18.6 |
| Spatial Extension | PostGIS 3.7.0 |
| Database Name | `karhutla_db` |
| Schema | `karhutla` |
| Coordinate Reference System | EPSG:4326 |
| Study Area | Five provinces in Kalimantan |
| Analysis Period | September 1–30, 2026 |

### 3. Database Backup

The database backup is provided in:

`01_Database/karhutla_db.backup`

- Backup Format: PostgreSQL Custom Format (`pg_dump -F c`)
- File Size: Approximately 22.74 MiB
- Backup Date: November 22, 2026

The backup contains the database schema, tables, records, constraints, indexes, and database objects included in the PostgreSQL backup.

### 4. Database Restoration

Before accessing the database, restore the provided backup into a PostgreSQL instance.

**Requirements:**

- PostgreSQL 18 or compatible version
- PostGIS 3.7 or compatible version
- `pg_restore` utility

**Restoration steps:**

1. Install PostgreSQL and PostGIS.
2. Create an empty database named `karhutla_db`.
3. Ensure the PostgreSQL user has sufficient privileges to restore the backup and create required database objects.
4. Restore `karhutla_db.backup` into the newly created database.

Example using PowerShell:

```powershell
pg_restore -U postgres -d karhutla_db -v "path\to\karhutla_db.backup"
```

If PostgreSQL's `bin` directory is not included in PATH, use the full path to `pg_restore.exe`.

For example:

```powershell
& "C:\Program Files\PostgreSQL\18\bin\pg_restore.exe" -U postgres -d karhutla_db -v "path\to\karhutla_db.backup"
```

**Important:**

- Restore into an empty database.
- Do not overwrite an existing database containing important data without creating a separate backup first.
- The backup was successfully tested by restoring it into a temporary database and verifying the table record counts and PostGIS version.

### 5. Database Connection

Use the following connection parameters:

| Parameter | Value |
|---|---|
| Host | `localhost` (local installation) |
| Port | `5432` (default) |
| Database | `karhutla_db` |
| Username | Your PostgreSQL username |
| Password | Your PostgreSQL password |
| Schema | `karhutla` |

For remote access, the host, port, username, and database permissions must be configured by the database administrator.

**Security Note:**

Database credentials must be shared securely and should never be committed to GitHub or included directly in SQL scripts or documentation.

### 6. Database Tables

The database contains five main tables with a total of 115,736 records.

| Table | Records | Description |
|---|---:|---|
| `karhutla.dim_provinces` | 5 | Provincial administrative boundaries |
| `karhutla.dim_peatlands` | 350 | Peatland spatial features |
| `karhutla.fact_hotspots` | 115,137 | FIRMS active fire detections |
| `karhutla.sentinel2_products` | 214 | Sentinel-2 product metadata and footprints |
| `karhutla.chirps_raster_metadata` | 30 | Daily CHIRPS raster metadata |

### 7. Basic SQL Queries

All queries should be executed after connecting to `karhutla_db`.

#### 7.1 List Available Tables

```sql
SELECT table_name
FROM information_schema.tables
WHERE table_schema = 'karhutla'
  AND table_type = 'BASE TABLE'
ORDER BY table_name;
```

#### 7.2 Count Records in Each Table

```sql
SELECT 'dim_provinces' AS table_name, COUNT(*) AS total_records
FROM karhutla.dim_provinces

UNION ALL

SELECT 'dim_peatlands', COUNT(*)
FROM karhutla.dim_peatlands

UNION ALL

SELECT 'fact_hotspots', COUNT(*)
FROM karhutla.fact_hotspots

UNION ALL

SELECT 'sentinel2_products', COUNT(*)
FROM karhutla.sentinel2_products

UNION ALL

SELECT 'chirps_raster_metadata', COUNT(*)
FROM karhutla.chirps_raster_metadata;
```

#### 7.3 Inspect Table Columns

Before writing analytical queries, inspect the actual column names and data types.

```sql
SELECT
    table_name,
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_schema = 'karhutla'
ORDER BY table_name, ordinal_position;
```

#### 7.4 Hotspot Detections by Province

The following query uses the existing `province_id` relationship in the database.

```sql
SELECT
    p.province_name,
    COUNT(h.hotspot_id) AS total_hotspots
FROM karhutla.dim_provinces p
LEFT JOIN karhutla.fact_hotspots h
    ON p.province_id = h.province_id
GROUP BY p.province_name
ORDER BY total_hotspots DESC;
```

#### 7.5 Daily Hotspot Detections

```sql
SELECT
    acq_date,
    COUNT(*) AS total_hotspots
FROM karhutla.fact_hotspots
GROUP BY acq_date
ORDER BY acq_date;
```

#### 7.6 Preview Sentinel-2 Product Records

```sql
SELECT *
FROM karhutla.sentinel2_products
LIMIT 5;
```

This query provides a preview of available Sentinel-2 metadata and helps identify the appropriate columns for further analysis.

### 8. Spatial Data Information

Spatial data is stored using PostGIS geometry types with EPSG:4326.

| Table | Geometry Column | Geometry Type |
|---|---|---|
| `dim_provinces` | `geom` | MultiPolygon |
| `dim_peatlands` | `geom` | MultiPolygon |
| `fact_hotspots` | `geom` | Point |
| `sentinel2_products` | `geom` | Polygon |

#### 8.1 Inspect Geometry Columns

Use the following query to identify geometry column names, geometry types, and SRIDs.

```sql
SELECT
    f_table_name,
    f_geometry_column,
    type,
    srid
FROM geometry_columns
WHERE f_table_schema = 'karhutla'
ORDER BY f_table_name;
```

#### 8.2 Spatial Join: Hotspots Within Peatland Areas

The following example counts hotspot detections located within peatland geometries.

```sql
SELECT
    COUNT(*) AS hotspots_in_peatland
FROM karhutla.fact_hotspots h
JOIN karhutla.dim_peatlands p
    ON ST_Within(h.geom, p.geom);
```

This query uses the actual geometry columns available in the database.

**Note:** A hotspot may be counted more than once if peatland geometries overlap. This query is an example of spatial analysis and should not be interpreted as a measure of burned area or fire severity.

### 9. External Raster Data

CHIRPS raster pixels are stored as GeoTIFF files rather than directly inside PostgreSQL.

The database table `karhutla.chirps_raster_metadata` stores raster metadata and file paths.

The daily raster files are available in:

`02_Datasets/chirps/daily/`

Analysts can use Python libraries such as Rasterio or GDAL to read and process these files.

### 10. Important Data Considerations

- FIRMS records represent satellite-based active fire detections, not confirmed fire incidents, burned area, or fire severity.
- Hotspot detections may contain multiple observations associated with the same fire event.
- Sentinel-2 records contain product metadata and spatial footprints, not downloaded satellite image pixels.
- Sentinel-2 cloud cover represents product-level metadata.
- CHIRPS raster data must be accessed from the shared dataset directory.
- All spatial layers use EPSG:4326.
- Peatland-province spatial relationships are available separately as a processed dataset; `dim_peatlands` does not have a direct province foreign key.
- FIRMS records that could not be matched to the five study provinces are not included in the main `fact_hotspots` table.

### 11. Related Documentation

For additional information, refer to:

- `03_Documentation/data_engineering_progress.md`
- `03_Documentation/data_dictionary.xlsx`
- `03_Documentation/data_sources.md`
- `04_Analysis_Handover/data_analytics_notes.md`

---

**Prepared by:** Data Engineering Team  
**Project:** Karhutla Spatial-Temporal Analysis  
**Last Updated:** November 22, 2026