# Peatland Distribution Data Dictionary

## 1. Dataset Overview

| Attribute | Description |
|---|---|
| Dataset Name | Kalimantan Peatland Distribution |
| Data Source | BNPB InAWARE / Global Forest Watch |
| Original Data Provider | World Resources Institute (WRI) |
| Source Service | Indonesia Peat Lands Feature Layer |
| Data Format | GeoJSON (raw and processed), CSV (spatial relationship) |
| Geometry Type | Polygon and MultiPolygon |
| Coordinate Reference System | EPSG:4326 |
| Study Area | Five provinces in Kalimantan, Indonesia |
| Number of Features | 350 |

**Source:** https://gis.bnpb.go.id/server/rest/services/InAWARE/Global_forest_watch2/MapServer/3

## 2. Dataset Description

This dataset represents the spatial distribution of peatland areas across the Kalimantan study area.

The data is obtained from the BNPB InAWARE / Global Forest Watch peatland layer, which provides polygon geometries representing peatland distribution in Indonesia.

The dataset is used to examine the spatial relationship between peatland areas, administrative boundaries, and fire hotspot detections.

The available attributes provide limited information about peatland classification. The dataset does not contain sufficient detailed information about peat depth, condition, or other physical characteristics.

## 3. Raw Dataset Structure

**Source file:**

`data/raw/peatland/peatland_kalimantan_bbox.geojson`

| Attribute | Description |
|---|---|
| Shape_Length | Source-provided geometry length attribute |
| Shape_Area | Source-provided geometry area attribute |
| OBJECTID_12 | Source feature identifier |
| objectid_1 | Source object identifier |
| objectid | Source object identifier |
| layer_revi | Source classification or layer revision attribute |
| shape_leng | Source-provided geometry length attribute |
| globalid | Global feature identifier |
| shape_Le_1 | Source-provided geometry length attribute |
| geometry | Peatland polygon geometry |

**Note:** The exact definitions and units of the source-provided numeric attributes should be confirmed against the original layer metadata before they are used for quantitative analysis.

## 4. Processed Dataset Structure

### Output Files

| File | Description |
|---|---|
| `data/processed/peatland/peatland_kalimantan_clean.geojson` | Cleaned peatland polygon dataset |
| `data/processed/peatland/peatland_province_relationship.csv` | Spatial relationship between peatland features and provincial boundaries |

### Processed GeoJSON

The cleaned GeoJSON retains the original source attributes and polygon geometries.

| Attribute | Description |
|---|---|
| Source attributes | Original attributes retained from the source dataset |
| layer_revi_clean | Normalized classification value derived from `layer_revi` |
| geometry | Validated peatland polygon geometry |

The `layer_revi_clean` attribute normalizes blank classification values into `unknown` while preserving the original `layer_revi` field.

## 5. Classification Information

The original `layer_revi` attribute contains the following values:

| Original Value | Record Count |
|---|---:|
| `gambut` | 348 |
| Blank value | 2 |
| **Total** | **350** |

The two blank values are normalized to `unknown` in the cleaned classification field.

Other categories found in the broader source layer include `gambut 40cm`, `gambut tipis`, and `tanah mineral (bukan ...)`. These categories were not present in the 350-feature Kalimantan subset.

**Important:** The meaning of the numeric suffix in `gambut 40cm` and the exact classification methodology have not been verified. These values should not be interpreted as measured peat depth without supporting metadata.

## 6. Spatial Processing

The raw peatland dataset was processed through the following steps:

1. Retrieve the peatland polygon data from the BNPB InAWARE / Global Forest Watch feature layer.
2. Select features within a bounding box covering the Kalimantan study area.
3. Convert the retrieved geometries to EPSG:4326.
4. Inspect attribute completeness and geometry validity.
5. Check for duplicate features and invalid geometries.
6. Normalize blank classification values in `layer_revi`.
7. Perform a spatial join with the five provincial administrative boundaries using the `intersects` predicate.
8. Export the cleaned polygon dataset and province relationship table.

The original polygon geometries are retained. They are not clipped to individual provincial boundaries.

## 7. Spatial Validation

| Validation | Result |
|---|---:|
| Total Features | 350 |
| Polygon Geometries | 345 |
| MultiPolygon Geometries | 5 |
| Null Attributes | None |
| Empty Geometries | 0 |
| Invalid Geometries | 0 |
| Duplicate Features | 0 |
| Coordinate Reference System | EPSG:4326 |

### Spatial Extent

| Attribute | Value |
|---|---:|
| Minimum Longitude | 108.855817 |
| Minimum Latitude | -3.477970 |
| Maximum Longitude | 118.583596 |
| Maximum Latitude | 4.076790 |

## 8. Relationship with Provincial Boundaries

A spatial join was performed between the peatland polygons and the five provincial administrative boundaries using the `intersects` predicate.

### Spatial Relationship Summary

| Province | Intersecting Peatland Features |
|---|---:|
| Kalimantan Barat | 178 |
| Kalimantan Tengah | 122 |
| Kalimantan Timur | 32 |
| Kalimantan Utara | 16 |
| Kalimantan Selatan | 5 |
| **Total Relationships** | **353** |

The spatial join produced 353 relationships from 350 unique peatland features.

Three peatland polygons intersect more than one province boundary:

- Object ID 1311: Kalimantan Tengah and Kalimantan Barat.
- Object ID 1341: Kalimantan Tengah and Kalimantan Barat.
- Object ID 1449: Kalimantan Selatan and Kalimantan Tengah.

Therefore, provincial relationship counts should not be interpreted as unique peatland feature counts that are mutually exclusive.

## 9. Usage in the Project

The processed peatland dataset supports:

- Identifying peatland distribution across the study area.
- Examining spatial relationships between peatland areas and fire hotspots.
- Associating peatland polygons with provincial administrative boundaries.
- Supporting spatial analysis of hotspot distribution in peatland ecosystems.

## 10. Important Notes and Limitations

1. The original peatland layer covers Indonesia; the project dataset is a subset retrieved using a Kalimantan bounding box.
2. A bounding-box selection does not guarantee that all retrieved polygons are completely contained within the five provincial boundaries.
3. The `intersects` spatial join identifies geometric intersections, not exclusive provincial ownership.
4. Source attributes are retained without assuming undocumented meanings or measurement units.
5. The two blank `layer_revi` values are classified as `unknown`, not automatically assumed to represent peatland or mineral soil.
6. The dataset does not provide sufficient verified information for direct peat-depth or peat-condition analysis.
7. The source dataset is an alternative to the desired detailed peatland map from the Ministry of Agriculture, which was inaccessible during data collection.

## 11. References

- BNPB InAWARE / Global Forest Watch Peatland Layer: https://gis.bnpb.go.id/server/rest/services/InAWARE/Global_forest_watch2/MapServer/3
- Global Forest Watch: https://www.globalforestwatch.org/