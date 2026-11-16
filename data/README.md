# Data Directory

This directory contains datasets used throughout the Karhutla Spatial-Temporal Analysis project.

## Directory Structure

| Folder | Description |
|---|---|
| `raw/` | Original datasets collected from external sources |
| `staging/` | Temporary datasets prepared for transformation |
| `processed/` | Cleaned and transformed datasets |
| `final/` | Final datasets ready for analytical purposes |

## Data Sources

- NASA FIRMS – Fire hotspot data
- CHIRPS – Rainfall data
- ERA5 – Weather data
- Sentinel-2 – Satellite imagery
- BIG / GADM – Administrative boundaries
- Peatland datasets – Peatland distribution

## Data Management Guidelines

1. Original datasets must remain unchanged in `raw/`.
2. Intermediate datasets are stored in `staging/`.
3. Cleaned datasets are stored in `processed/`.
4. Validated datasets ready for analysis are stored in `final/`.
5. Sensitive credentials and API keys must never be committed to GitHub.

**Note:** Large datasets are not necessarily stored directly in this repository. Refer to their source links and data documentation.