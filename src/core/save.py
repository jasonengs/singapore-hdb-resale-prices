from pathlib import Path

import geopandas as gpd
import pandas as pd


def save_to_csv(df: pd.DataFrame, name: str, path: Path) -> None:
    # Define filename
    filename = f"{name}.csv"
    # Construct the full path
    output_path = path / filename
    # Save as csv file
    df.to_csv(output_path, index=False)


def save_to_geojson(gdf: gpd.GeoDataFrame, name: str, path: Path) -> None:
    # Define filename
    filename = f"{name}.geojson"
    # Construct the full path
    output_path = path / filename
    # Save as geojson file
    gdf.to_file(output_path, driver="GeoJSON")
