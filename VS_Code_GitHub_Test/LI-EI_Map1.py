import pandas as pd
import geopandas as gpd
from shapely.geometry import Point
from pathlib import Path
import folium

# ---------------------------------------------------
# FILE PATHS - relative to this script
# ---------------------------------------------------

# Folder containing THIS .py file
HERE = Path(__file__).resolve().parent

# Data folder inside the repo
DATA = HERE / "data"

excel_path = DATA / "LI-EI.xlsx"
output_map = HERE / "hounslow_income_acorn_map.html"

hounslow_boundary = DATA / "Hounslow_boundary.geojson"
ward_boundaries = None  # enable later if needed

# ---------------------------------------------------
# COLUMN NAMES
# ---------------------------------------------------
EASTING = "easting"
NORTHING = "northing"
ACORN = "Acorn Classification (Household)"
MED_INC = "Median Income (PC)"

# ---------------------------------------------------
# LOAD + CLEAN
# ---------------------------------------------------
df = pd.read_excel(excel_path)
df.columns = df.columns.str.strip()

df = df.dropna(subset=[EASTING, NORTHING]).copy()
df[EASTING] = pd.to_numeric(df[EASTING], errors="coerce")
df[NORTHING] = pd.to_numeric(df[NORTHING], errors="coerce")
df = df.dropna(subset=[EASTING, NORTHING])

# ---------------------------------------------------
# CONVERT TO GEO
# ---------------------------------------------------
gdf = gpd.GeoDataFrame(
    df,
    geometry=[Point(xy) for xy in zip(df[EASTING], df[NORTHING])],
    crs="EPSG:27700"
).to_crs(epsg=4326)

# ---------------------------------------------------
# CREATE MAP
# ---------------------------------------------------
center_lat = float(gdf.geometry.y.mean())
center_lon = float(gdf.geometry.x.mean())

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=12,
    tiles="cartodbpositron"
)

# ---------------------------------------------------
# ADD BOROUGH OUTLINE
# ---------------------------------------------------
if hounslow_boundary.exists():
    borough = gpd.read_file(hounslow_boundary).to_crs(epsg=4326)
    folium.GeoJson(
        borough,
        name="Hounslow Borough",
        style_function=lambda x: {"fillColor": "none", "color": "blue", "weight": 2},
    ).add_to(m)

# ---------------------------------------------------
# OPTIONAL: ADD WARD BOUNDARIES
# ---------------------------------------------------
