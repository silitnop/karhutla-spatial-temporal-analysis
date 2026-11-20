# CHIRPS Rainfall Data Dictionary

## 1. Dataset Overview

| Attribute | Description |
|---|---|
| Dataset Name | Daily Rainfall |
| Data Source | Climate Hazards Center InfraRed Precipitation with Station Data (CHIRPS) |
| Product Version | CHIRPS v3.0 |
| Product Type | Daily Final SAT |
| Data Format | GeoTIFF (.tif) |
| Spatial Data Type | Raster |
| Coordinate Reference System | EPSG:4326 |
| Spatial Resolution | Approximately 0.05° |
| Observation Period | September 1–30, 2026 |
| Study Area | Five provinces in Kalimantan, Indonesia |
| Number of Daily Rasters | 30 |

**Source:** https://data.chc.ucsb.edu/products/CHIRPS/v3.0/

## 2. Dataset Description

CHIRPS is a satellite-based precipitation dataset developed by the Climate Hazards Center.

The dataset provides daily rainfall estimates by combining satellite observations with precipitation information from other sources.

This project uses the CHIRPS v3.0 Daily Final SAT product to represent daily rainfall conditions across the five provinces in Kalimantan during September 2026.

The raster pixel values represent estimated daily precipitation amounts.

## 3. Raw Dataset Structure

**Source directory:**

`data/raw/chirps/`

### File Naming Convention

`chirps-v3.0.sat.2026.09.DD.tif`

Where:

| Component | Description |
|---|---|
| `chirps-v3.0` | CHIRPS product version |
| `sat` | Satellite-based daily estimate |
| `2026` | Observation year |
| `09` | Observation month |
| `DD` | Observation day |
| `.tif` | GeoTIFF raster format |

### Raw Dataset Characteristics

| Attribute | Value |
|---|---|
| Number of Files | 30 |
| Total File Size | Approximately 448.72 MB |
| CRS | EPSG:4326 |
| Spatial Resolution | Approximately 0.05° |
| Raster Width | 7,200 pixels |
| Raster Height | 2,400 pixels |
| Number of Bands | 1 |
| Data Type | Float32 |
| Global Spatial Extent | Approximately -180° to 180° longitude and -60° to 60° latitude |

## 4. Raster Data Structure

Unlike tabular datasets, CHIRPS stores rainfall values in raster pixels rather than conventional rows and columns of attributes.

| Attribute | Description | Unit |
|---|---|---|
| Pixel Value | Estimated daily precipitation at a raster cell | Millimeters per day (mm/day) |
| NoData | Pixel without a valid observation | -9999 in the processed raster |
| Band 1 | Daily rainfall estimate | mm/day |

Each GeoTIFF file represents rainfall estimates for one observation date.

## 5. Processed Dataset Structure

**Output directory:**

`data/processed/chirps/daily/`

### Processing Summary

The raw CHIRPS rasters were processed through the following steps:

1. Check the completeness of daily raster files for September 1–30, 2026.
2. Inspect raster metadata, including CRS, resolution, dimensions, and data type.
3. Load the five provincial administrative boundary geometries.
4. Crop and mask each daily raster using the study area boundaries.
5. Assign `-9999` as the NoData value for pixels outside the study area.
6. Validate the resulting raster files.
7. Export the processed GeoTIFF files.

### Processed Raster Characteristics

| Attribute | Value |
|---|---|
| Number of Files | 30 |
| CRS | EPSG:4326 |
| Spatial Resolution | Approximately 0.05° |
| Raster Width | 210 pixels |
| Raster Height | 188 pixels |
| Number of Bands | 1 |
| Data Type | Float32 |
| NoData Value | -9999 |
| Pixels Inside Study Area | 17,373 per day |

## 6. Data Quality and Validation

The processed raster dataset was checked for:

| Validation | Result |
|---|---|
| Expected Daily Files | 30 |
| Available Daily Files | 30 |
| Missing Dates | 0 |
| Unexpected Dates | 0 |
| CRS Consistency | EPSG:4326 |
| Resolution Consistency | Approximately 0.05° |
| Valid Pixels Inside Study Area | 17,373 per day |
| Missing Pixels Inside Study Area | 0 per day |

All 30 daily rasters passed the file completeness and spatial validation checks.

### Sample Raster Statistics

The following statistics are from the processed September 1, 2026 raster:

| Statistic | Value |
|---|---:|
| Minimum | 0.00 mm/day |
| Maximum | 34.79 mm/day |
| Mean | 0.50 mm/day |
| Valid Pixels | 17,373 |
| Missing Pixels Inside Study Area | 0 |

These statistics describe the sample date only and should not be interpreted as monthly rainfall statistics.

## 7. Usage in the Project

The processed CHIRPS dataset supports:

- Examining daily rainfall patterns across the study area.
- Integrating rainfall information with fire hotspot observations.
- Investigating temporal relationships between rainfall and hotspot occurrence.
- Providing environmental context for downstream spatial-temporal analysis.
- Preparing daily rainfall features for analytical data integration.

## 8. Important Notes and Limitations

1. CHIRPS provides estimated precipitation values, not direct ground-based rainfall measurements at every raster pixel.
2. The spatial resolution is approximately 0.05°, so localized rainfall variations may not be fully represented.
3. The processed rasters retain the original geographic coordinate reference system and spatial resolution.
4. Pixels outside the study area are masked and assigned the NoData value `-9999`.
5. The zero missing-pixel result applies to pixels inside the study area, not the entire rectangular raster extent.
6. CHIRPS SAT daily estimates use IMERG Late V07 to disaggregate pentad precipitation totals into daily estimates. This should be considered when interpreting daily rainfall values.
7. The 30 daily files represent September 2026 only and do not provide long-term rainfall climatology.

## 9. References

- Climate Hazards Center: https://www.chc.ucsb.edu/data
- CHIRPS v3.0 Data Repository: https://data.chc.ucsb.edu/products/CHIRPS/v3.0/
- CHIRPS v3.0 Daily Final Documentation: https://data.chc.ucsb.edu/products/CHIRPS/v3.0/daily/final/readme.txt