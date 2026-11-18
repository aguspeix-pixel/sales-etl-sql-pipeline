# Automated Sales ETL & SQL Reporting Pipeline

Automated Python & SQLite solution that consolidates messy CSV sales files from multiple branches, cleans and standardizes data, stores records in a relational database, and generates a multi-sheet executive Excel report.

## Business Problem Solved
Many businesses waste hours manually merging spreadsheets, fixing inconsistent product names, removing duplicates, and calculating totals. This pipeline reduces a repetitive manual task to a **2-second automated execution**.

## Key Features
* **Multi-file Ingestion:** Automatically reads and merges all CSV files from the input directory.
* **Data Cleaning (`pandas`):** Standardizes text formatting, parses mixed date formats, removes currency symbols, handles missing values, and drops duplicates.
* **SQL Storage (`SQLite`):** Loads clean records into a structured SQL database for reliable querying.
* **Automated Reporting (`openpyxl`):** Runs SQL aggregations and exports a clean Excel workbook with 3 tabs: Clean Data, Sales by Product, and Sales by Branch.

## Tech Stack
* **Python 3**
* **pandas** (Data manipulation & cleaning)
* **SQLite3** (Relational database & SQL aggregations)
* **openpyxl** (Automated Excel report generation)

## How to Run
1. Install dependencies: `pip install pandas openpyxl`
2. Generate sample dirty data: `python generar_datos_prueba.py`
3. Run the ETL pipeline: `python pipeline_ventas.py`