import asyncio

import aiohttp
import geopandas as gpd
from aiolimiter import AsyncLimiter

from core.api import fetch_geo_data
from core.config import HEADERS_DATA_GOV_SG, APIConfig
from core.path import get_data_path
from core.save import save_to_geojson
from schemas.geojson import PlnAreaFeatureCollection, RegionFeatureCollection

DATASETS = {
    "region": {
        "id": "d_4ce0038f7ac689652350bb91b7fb92ed",
        "model": RegionFeatureCollection,
    },
    "pln_area": {
        "id": "d_2cc750190544007400b2cfd5d7f53209",
        "model": PlnAreaFeatureCollection,
    },
}


async def get_geo_data(config: APIConfig, geo_type: str) -> gpd.GeoDataFrame:
    geo_config = DATASETS[geo_type]
    geojson = await fetch_geo_data(config, geo_config["id"])

    validated = geo_config["model"].model_validate(geojson)
    gdf = gpd.GeoDataFrame.from_features(
        validated.model_dump()["features"], crs="EPSG:4326"
    )

    return gdf


async def main() -> None:
    limiter = AsyncLimiter(8, 10)
    data_dir = get_data_path()

    async with aiohttp.ClientSession(headers=HEADERS_DATA_GOV_SG) as session:
        config = APIConfig(session, limiter)

        region_gdf, pln_area_gdf = await asyncio.gather(
            get_geo_data(config, "region"), get_geo_data(config, "pln_area")
        )

    save_to_geojson(region_gdf, "region", data_dir)
    save_to_geojson(pln_area_gdf, "pln_area", data_dir)


if __name__ == "__main__":
    asyncio.run(main())
