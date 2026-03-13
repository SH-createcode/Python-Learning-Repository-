import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import folium

# ---------------------------------------------------
# PATH HANDLING (robust)
# ---------------------------------------------------

# Folder where THIS script lives
HERE = Path(__file__).resolve().parent

# Data folder inside VS_Code_GitHub_Test/
DATA = HERE / "data"

# Input files
excel_path = DATA / "LI-EI.xlsx"
boundary_path = DATA / "Hounslow_boundary.geojson"   # optional

# Output HTML file
output_map = HERE / "hounslow_income_acorn_map.html"

# Debug prints
print("Excel path:", excel_path)
print("Output map path:", output_map)
print("Boundary path:", boundary_path)

# ---------------------------------------------------
# COLUMN NAMES (must match your Excel sheet)
# ---------------------------------------------------
EASTING = "easting"
NORTHING = "northing"
ACORN = "Acorn Classification (Household)"
MED_INC = "Median Income (PC)"

# ---------------------------------------------------
# LOAD DATA
# ---------------------------------------------------
df = pd.read_excel(excel_path)
df.columns = df.columns.str.strip()

# Keep only valid coordinate rows
df = df.dropna(subset=[EASTING, NORTHING]).copy()
df[EASTING] = pd.to_numeric(df[EASTING], errors="coerce")
df[NORTHING] = pd.to_numeric(df[NORTHING], errors="coerce")
df = df.dropna(subset=[EASTING, NORTHING])

# ---------------------------------------------------
# CONVERT TO GEO
# ---------------------------------------------------
