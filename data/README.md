# Data Directory

This directory contains datasets used throughout the **Karhutla Spatial-Temporal Analysis** project.

The datasets provide spatial, temporal, and environmental information to support the analysis of forest and land fire patterns across five provinces in Kalimantan, Indonesia.

## Directory Structure

| Folder | Description |
|---|---|
| `raw/` | Original datasets collected from external sources |
| `staging/` | Temporary datasets prepared for transformation and integration |
| `processed/` | Cleaned, transformed, and validated datasets |
| `final/` | Integrated datasets prepared for downstream analytical purposes |

## Data Sources

### Available Datasets

| Dataset | Data Source | Description |
|---|---|---|
| Fire Hotspots | NASA FIRMS | Satellite-based thermal anomaly detections |
| Rainfall | CHIRPS v3.0 | Daily satellite-based rainfall estimates |
| Administrative Boundaries | BIG | Provincial administrative boundaries |
| Peatland Distribution | BNPB InAWARE / Global Forest Watch | Peatland spatial distribution |

### Planned Datasets

| Dataset | Data Source | Description |
|---|---|---|
| Weather Variables | ERA5 / ERA5-Land | Additional atmospheric and environmental variables |
| Satellite Imagery | Sentinel-2 | Multispectral imagery for vegetation and fire-related change analysis |

## Study Area and Observation Period

- **Study Area:** Five provinces in Kalimantan, Indonesia.
- **Observation Period:** September 1–30, 2026.

The study area includes:

- West Kalimantan
- Central Kalimantan
- South Kalimantan
- East Kalimantan
- North Kalimantan

## Data Management Guidelines

1. Original datasets must remain unchanged in `raw/`.
2. Intermediate datasets are stored in `staging/`.
3. Cleaned and transformed datasets are stored in `processed/`.
4. Integrated and validated datasets ready for analysis are stored in `final/`.
5. Sensitive credentials and API keys must never be committed to GitHub.
6. Each dataset should include documentation describing its source, format, coordinate reference system, and processing history.

## Data Storage and Version Control

Large datasets are not necessarily stored directly in this repository due to GitHub file size limitations.

Original datasets may be maintained in external storage, while source links, metadata, processing scripts, and documentation are maintained in this repository.

Refer to the respective dataset documentation for additional information.

## Notes

- All processed vector datasets use EPSG:4326 as the common geographic coordinate reference system where applicable.
- Raster datasets retain their spatial resolution and coordinate reference system during processing unless explicitly transformed.
- Dataset availability may change as the project progresses.
- The `final/` directory will contain integrated datasets after the data integration stage is completed.