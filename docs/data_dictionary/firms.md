# FIRMS Hotspot Data Dictionary

## 1. Dataset Overview

| Attribute | Description |
|---|---|
| Dataset Name | Fire Hotspots |
| Data Source | NASA Fire Information for Resource Management System (FIRMS) |
| Satellite | Suomi-NPP (SNPP) |
| Product | VIIRS S-NPP Collection 2 Near Real-Time (NRT) |
| Product Version | 2.0NRT |
| Data Format | CSV (raw), CSV and GeoJSON (processed) |
| Observation Period | September 1–30, 2026 (analysis period) |
| Raw Data Coverage | September 1–October 31, 2026 |
| Study Area | Five provinces in Kalimantan, Indonesia |
| Coordinate Reference System | EPSG:4326 for processed spatial data |

**Source:** https://firms.modaps.eosdis.nasa.gov/

## 2. Dataset Description

The dataset contains satellite-based active fire and thermal anomaly detections collected by NASA FIRMS.

Each record represents an individual hotspot detection with associated geographic coordinates, acquisition time, thermal measurements, fire radiative power, and detection confidence information.

Hotspot detections indicate potential fire activity or thermal anomalies. They do not directly represent fire perimeters, burned areas, or fire severity.

## 3. Raw Dataset Structure

**Source file:**

`data/raw/firms/fire_nrt_SV-C2_852079.csv`

| Column | Data Type | Description | Unit / Notes |
|---|---|---|---|
| latitude | Float | Latitude of the hotspot detection | Decimal degrees |
| longitude | Float | Longitude of the hotspot detection | Decimal degrees |
| brightness | Float | Brightness temperature measurement associated with the detection | Kelvin (K); exact channel mapping requires verification |
| scan | Float | Scan dimension associated with the satellite observation | Product-specific measurement |
| track | Float | Track dimension associated with the satellite observation | Product-specific measurement |
| acq_date | Date | Date of satellite observation | YYYY-MM-DD |
| acq_time | Integer | Time of satellite observation | HHMM format; verify time-zone convention against product documentation |
| satellite | String | Satellite identifier | SNPP |
| instrument | String | Instrument field as recorded in the source CSV | SNPP |
| confidence | String | Confidence classification of the hotspot detection | `l`, `n`, `h` |
| version | String | FIRMS processing version | 2.0NRT |
| bright_t31 | Float | Additional brightness temperature measurement | Kelvin (K); exact channel mapping requires verification |
| frp | Float | Fire Radiative Power | Megawatts (MW) |
| daynight | String | Day or night observation indicator | `D` = Day, `N` = Night |

**Note:** The source CSV uses `brightness` and `bright_t31` rather than the commonly documented VIIRS field names `bright_ti4` and `bright_ti5`. Their exact channel correspondence has not yet been verified. Original column names are retained without modification.

## 4. Confidence Classification

The `confidence` column represents the detection confidence category.

| Value | Description |
|---|---|
| `l` | Low confidence |
| `n` | Nominal confidence |
| `h` | High confidence |

These categories are classification labels, not direct probabilities that a fire is occurring.

## 5. Raw Dataset Profile

| Attribute | Value |
|---|---:|
| Total Records | 210,915 |
| Total Columns | 14 |
| Satellite | SNPP |
| Instrument Field | SNPP |
| Product Version | 2.0NRT |
| Raw Date Range | September 1–October 31, 2026 |

### Confidence Distribution

| Confidence | Records |
|---|---:|
| Nominal (`n`) | 196,569 |
| Low (`l`) | 7,760 |
| High (`h`) | 6,586 |
| **Total** | **210,915** |

## 6. Processed Dataset Structure

The raw dataset is processed to select observations within the study period and spatial extent.

### Output Files

| File | Description |
|---|---|
| `data/processed/firms/hotspots_kalimantan_september_2026.csv` | Filtered hotspot records within the study area |
| `data/processed/firms/hotspots_kalimantan_september_2026.geojson` | Spatial representation of hotspot detections |
| `data/processed/firms/hotspots_outside_study_area_september_2026.csv` | Records not matched to the five selected provincial boundaries |

### Processing Summary

| Processing Step | Description |
|---|---|
| Date Filtering | Select observations from September 1–30, 2026 |
| Spatial Filtering | Identify hotspot detections within the five Kalimantan provinces |
| Spatial Conversion | Convert geographic coordinates into point geometries |
| Spatial Join | Associate hotspot points with provincial administrative boundaries |
| Output Generation | Export filtered records into CSV and GeoJSON formats |

### Spatial Join Summary

| Result | Records |
|---|---:|
| Total September Hotspots | 115,739 |
| Matched to Provincial Boundaries | 115,137 |
| Unmatched to Selected Boundaries | 602 |

Unmatched records are retained separately for further inspection. They should not automatically be interpreted as detections outside Indonesia.

## 7. Data Quality and Validation

The raw and processed datasets were checked for:

- Missing values in the raw dataset.
- Duplicate records.
- Invalid geographic coordinates.
- Negative Fire Radiative Power values.
- Observations outside the selected analysis period.
- Spatial matching against the five provincial boundaries.

The processed dataset retains the original source attributes while adding spatial information for geographic analysis.

## 8. Important Notes and Limitations

1. FIRMS hotspot detections represent satellite-observed thermal anomalies, not confirmed fire perimeters.
2. Hotspot counts should not be interpreted directly as burned area or fire severity.
3. The confidence field contains categorical values (`l`, `n`, and `h`).
4. The exact channel mapping of `brightness` and `bright_t31` requires further verification against the source product schema.
5. Unmatched hotspot records are preserved separately rather than automatically discarded.
6. The raw dataset is retained unchanged to preserve source integrity.

## 9. References

- NASA FIRMS: https://firms.modaps.eosdis.nasa.gov/
- FIRMS Download Readme: https://firms.modaps.eosdis.nasa.gov/download/Readme.txt
- NASA FIRMS Data Format Information: https://firms.modaps.eosdis.nasa.gov/content/academy/data_format.html