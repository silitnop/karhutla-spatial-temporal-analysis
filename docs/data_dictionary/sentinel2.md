# Sentinel-2 Data Dictionary

## 1. Dataset Overview

| Attribute | Description |
|---|---|
| Dataset Name | Sentinel-2 Level-2A |
| Data Provider | Copernicus Data Space Ecosystem |
| Data Source | Copernicus STAC API |
| STAC Collection | `sentinel-2-l2a` |
| Observation Period | September 1–30, 2026 |
| Study Area | Five provinces in Kalimantan, Indonesia |
| Coordinate Reference System | EPSG:4326 |
| Data Format | GeoJSON and CSV |
| Processing Stage | Raw and Staging |

## 2. Data Acquisition

Sentinel-2 product metadata was retrieved through the Copernicus Data Space STAC API.

The search used the study area's bounding box and the following filters:

- Observation period: September 1–30, 2026.
- Maximum cloud cover: 30%.
- Spatial filtering: product footprints intersecting the Kalimantan study area.

The initial STAC search returned 599 products. After filtering by intersection with the study area, 214 products remained, representing 61 unique MGRS tiles.

**Note:** The spatial intersection filter identifies products whose footprints intersect the study area. It does not guarantee that the entire product footprint is located within the study area.

## 3. File Structure

| File | Directory | Description |
|---|---|---|
| `sentinel2_september_2026_stac_search.geojson` | `data/raw/sentinel2/` | Original STAC search response containing 599 product features |
| `sentinel2_september_2026_metadata.csv` | `data/staging/sentinel2/` | Filtered product metadata containing 214 records |
| `sentinel2_september_2026_tile_summary.csv` | `data/staging/sentinel2/` | Summary of Sentinel-2 products grouped by MGRS tile |
| `sentinel2_september_2026_footprints.geojson` | `data/staging/sentinel2/` | Spatial footprints of the 214 filtered products |

## 4. Metadata Attributes

The metadata CSV contains eight attributes for each Sentinel-2 product.

| Attribute | Description |
|---|---|
| `product_id` | Unique identifier of the Sentinel-2 product |
| `datetime` | Acquisition date and time of the satellite observation |
| `cloud_cover` | Overall cloud cover percentage reported for the product |
| `mgrs_tile` | Military Grid Reference System tile identifier |
| `platform` | Satellite platform used to acquire the imagery |
| `instruments` | Instrument used to capture the satellite observation |
| `processing_level` | Processing level of the Sentinel-2 product |
| `collection` | STAC collection identifier associated with the product |

The product footprint geometry is stored separately in `sentinel2_september_2026_footprints.geojson`, rather than in the metadata CSV.

## 5. Tile Summary Attributes

The tile summary CSV aggregates Sentinel-2 product metadata by MGRS tile.

| Attribute | Description |
|---|---|
| `mgrs_tile` | Unique MGRS tile identifier |
| `total_products` | Total number of products associated with the tile |
| `min_cloud_cover` | Minimum cloud cover percentage among products in the tile |
| `mean_cloud_cover` | Average cloud cover percentage among products in the tile |
| `max_cloud_cover` | Maximum cloud cover percentage among products in the tile |
| `first_date` | Earliest acquisition datetime recorded for the tile |
| `last_date` | Latest acquisition datetime recorded for the tile |

The summary helps identify tiles with multiple observations and compare their cloud cover conditions during September 2026.

## 6. Data Quality Validation

The following checks were performed after metadata extraction:

| Validation | Result |
|---|---:|
| Products returned by STAC search | 599 |
| Products intersecting study area | 214 |
| Unique products | 214 |
| Unique MGRS tiles | 61 |
| Missing product IDs | 0 |
| Missing acquisition datetime | 0 |
| Missing cloud cover values | 0 |
| Missing footprint geometries | 0 |
| Invalid footprint geometries | 0 |
| Metadata and footprint counts match | Yes |

## 7. Cloud Cover Statistics

Cloud cover statistics for the 214 filtered products:

| Statistic | Value (%) |
|---|---:|
| Minimum | 0.58 |
| First Quartile (Q1) | 9.87 |
| Median | 17.68 |
| Mean | 16.67 |
| Third Quartile (Q3) | 23.28 |
| Maximum | 29.95 |
| Standard Deviation | 8.08 |

**Note:** Cloud cover represents the product-level estimate and does not necessarily reflect the actual cloud conditions over the specific area of interest.

## 8. Data Limitations

- The current dataset contains product metadata and spatial footprints, not downloaded Sentinel-2 raster imagery.
- No vegetation indices such as NDVI, NBR, or dNBR have been calculated at this stage.
- The September 2026 observation period alone is insufficient for a complete pre-fire and post-fire comparison.
- Product footprints may extend beyond the study area.
- Cloud cover values are product-level estimates and should not be interpreted as local cloud percentages.

## 9. Intended Use

Sentinel-2 Level-2A imagery is intended to support further spatial analysis of vegetation conditions and potential burn scars.

After selecting and downloading suitable imagery, the raster data may be processed to derive vegetation indices such as NDVI and NBR. Pre-fire and post-fire observations can then be compared to calculate dNBR, subject to image availability and quality.

The resulting imagery and derived datasets will support the analytical stage of the Karhutla Spatial-Temporal Analysis project.