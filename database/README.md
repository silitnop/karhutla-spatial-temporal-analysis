# Database Documentation

This directory contains SQL scripts and database documentation for the Karhutla Spatial-Temporal Analysis project.

The project uses **PostgreSQL** and **PostGIS** to store, manage, transform, and analyze geospatial data related to forest and land fires across five provinces in Kalimantan, Indonesia.

## Directory Structure

```text
database/
├── schema/
├── staging/
├── analytical_mart/
└── README.md
```

### 1. Schema

Contains SQL scripts for defining the database structure, including table creation, relationships, primary keys, foreign keys, and indexes.

### 2. Staging

Contains SQL scripts for temporary data storage and preparation before data is loaded into the analytical database.

Typical operations include:
- Data type conversion
- Duplicate checking
- Data validation
- Data transformation

### 3. Analytical Mart

Contains SQL scripts for creating analytical tables and dimensional models used by the Data Analytics team.

The analytical mart is designed to support:
- Hotspot distribution analysis
- Spatial-temporal clustering
- Environmental factor analysis
- Fire severity analysis and prediction
- Dashboard data preparation

## Database Technology

| Component | Technology |
|---|---|
| Database Management System | PostgreSQL |
| Geospatial Extension | PostGIS |
| Query Language | SQL |
| Database Client | DBeaver |
| Python Integration | SQLAlchemy / Psycopg |

## Data