import json
from functools import cache

import geopandas as gpd

from core.path import get_data_path


@cache
def load_gdf(layer: str) -> gpd.GeoDataFrame:
    gdf = gpd.read_file(get_data_path() / f"{layer}.geojson")

    return gdf


@cache
def load_geojson(layer: str) -> dict:
    gdf = load_gdf(layer)

    geojson = json.loads(gdf.to_json())

    return geojson
