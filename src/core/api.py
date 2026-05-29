import asyncio
from itertools import chain
from typing import TypeVar

from core.config import APIConfig
from core.constants import BASE_URL, LIMIT
from schemas.hdb import Flat, PriceIndex

T = TypeVar("T", Flat, PriceIndex)


async def get_response(
    config: APIConfig, url: str, content_type: str = "application/json"
) -> dict:
    async with config.limiter:
        async with config.session.get(url) as response:
            result = await response.json(content_type=content_type)

            return result


# Fetch dataset id specifically for resale price dataset as it has more than one file
async def fetch_dataset_id(
    config: APIConfig,
) -> list[str]:
    collection_id = 189
    url = f"https://api-production.data.gov.sg/v2/public/api/collections/{collection_id}/metadata"
    result = await get_response(config, url)

    data = result["data"]["collectionMetadata"]["childDatasets"]

    return data


async def get_total(config: APIConfig, dataset_id: str) -> int:
    url = f"{BASE_URL}?resource_id={dataset_id}"
    data = await get_response(config, url)
    total = data["result"]["total"]

    return total


async def fetch_page(config: APIConfig, dataset_id: str, offset: int) -> list[dict]:
    url = f"{BASE_URL}?resource_id={dataset_id}&offset={offset}&limit={LIMIT}"

    data = await get_response(config, url)

    records = data["result"]["records"]

    return records


async def fetch_latest_data(config: APIConfig, dataset_id: str) -> list[dict]:
    total = await get_total(config, dataset_id)

    tasks = [
        fetch_page(config, dataset_id, offset) for offset in range(0, total, LIMIT)
    ]

    pages = await asyncio.gather(*tasks)
    records = list(chain.from_iterable(pages))

    return records


async def fetch_geo_data(config: APIConfig, dataset_id: str) -> dict:
    url = f"https://api-open.data.gov.sg/v1/public/api/datasets/{dataset_id}/poll-download"

    response = await get_response(config, url)

    geojson_url = response["data"]["url"]

    geojson = await get_response(config, geojson_url, content_type=None)

    return geojson
