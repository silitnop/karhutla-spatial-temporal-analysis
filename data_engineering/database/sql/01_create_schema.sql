
-- =====================================================
-- KARHUTLA SPATIAL-TEMPORAL ANALYSIS
-- DATABASE SCHEMA
-- PostgreSQL 18 + PostGIS 3.7
-- =====================================================

-- 1. Enable PostGIS
CREATE EXTENSION IF NOT EXISTS postgis;

-- 2. Create schema
CREATE SCHEMA IF NOT EXISTS karhutla;

-- 3. Provinces
CREATE TABLE IF NOT EXISTS karhutla.dim_provinces (
    province_id SMALLINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    province_name VARCHAR(100) NOT NULL UNIQUE,
    geom geometry(MultiPolygon, 4326) NOT NULL
);

-- 4. Peatlands
CREATE TABLE IF NOT EXISTS karhutla.dim_peatlands (
    peatland_id INTEGER PRIMARY KEY,
    source_objectid_12 INTEGER,
    source_objectid_1 INTEGER,
    layer_revi VARCHAR(100),
    layer_revi_clean VARCHAR(100),
    globalid VARCHAR(100),
    shape_length DOUBLE PRECISION,
    shape_area DOUBLE PRECISION,
    geom geometry(MultiPolygon, 4326) NOT NULL
);

-- 5. FIRMS hotspots
CREATE TABLE IF NOT EXISTS karhutla.fact_hotspots (
    hotspot_id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    latitude DOUBLE PRECISION NOT NULL CHECK(latitude BETWEEN -90 AND 90),
    longitude DOUBLE PRECISION NOT NULL  CHECK (longitude BETWEEN -180 AND 180),
    brightness DOUBLE PRECISION,
    scan DOUBLE PRECISION,
    track DOUBLE PRECISION,
    acq_date DATE NOT NULL,
    acq_time INTEGER NOT NULL,
    satellite VARCHAR(30),
    instrument VARCHAR(30),
    confidence VARCHAR(20),
    version VARCHAR(30),
    bright_t31 DOUBLE PRECISION,
    frp DOUBLE PRECISION CHECK(frp >= 0),
    daynight CHAR(1),
    province_id SMALLINT REFERENCES karhutla.dim_provinces(province_id),
    geom GEOMETRY(POINT, 4326) NOT NULL
);

-- 6. Sentinel-2 products and footprints
CREATE TABLE IF NOT EXISTS karhutla.sentinel2_products (
    product_id VARCHAR(150) PRIMARY KEY,
    acquisition_datetime TIMESTAMPTZ NOT NULL,
    cloud_cover DOUBLE PRECISION CHECK(
        cloud_cover >= 0 AND cloud_cover <= 100
    ),
    mgrs_tile VARCHAR(20),
    platform VARCHAR(30),
    instruments VARCHAR(50),
    processing_level VARCHAR(20),
    collection VARCHAR(50),
    geom GEOMETRY(POLYGON, 4326) NOT NULL
);

-- 7. CHIRPS raster metadata
CREATE TABLE IF NOT EXISTS karhutla.chirps_raster_metadata (
    raster_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    raster_date DATE NOT NULL UNIQUE,
    file_name VARCHAR(255) NOT NULL UNIQUE,
    file_path TEXT NOT NULL,
    crs VARCHAR(30),
    width INTEGER,
    height INTEGER,
    band_count SMALLINT,
    resolution_x DOUBLE PRECISION,
    resolution_y DOUBLE PRECISION,
    nodata_value DOUBLE PRECISION,
    min_value DOUBLE PRECISION,
    max_value DOUBLE PRECISION,
    mean_value DOUBLE PRECISION
);

-- 8. Spatial indexes
CREATE INDEX IF NOT EXISTS idx_provinces_geom
ON karhutla.dim_provinces USING GIST (geom);

CREATE INDEX IF NOT EXISTS idx_peatlands_geom
ON karhutla.dim_peatlands USING GIST (geom);

CREATE INDEX IF NOT EXISTS idx_hotspots_geom
ON karhutla.fact_hotspots USING GIST (geom);

CREATE INDEX IF NOT EXISTS idx_sentinel2_geom
ON karhutla.sentinel2_products USING GIST (geom);

-- 9. Analytical indexes
CREATE INDEX IF NOT EXISTS idx_hotspots_acq_date
ON karhutla.fact_hotspots (acq_date);

CREATE INDEX IF NOT EXISTS idx_hotspots_province
ON karhutla.fact_hotspots (province_id);

CREATE INDEX IF NOT EXISTS idx_sentinel2_datetime
ON karhutla.sentinel2_products (acquisition_datetime);
