import asyncio
import re
import unicodedata

import aiohttp
import numpy as np
import pandas as pd
from aiolimiter import AsyncLimiter
from pydantic import TypeAdapter

from core.api import fetch_geo_data
from core.config import HEADERS_DATA_GOV_SG, HEADERS_GOOGLE_MAPS, APIConfig
from core.constants import GOOGLE_MAPS_PLACES_URL, PRIMARY_TYPES
from core.path import get_data_path
from core.save import save_to_csv
from core.transform import add_coords
from schemas.google import Place, Places
from schemas.hdb import Mrt


def normalize_name(text: str) -> str:
    text = unicodedata.normalize("NFKD", text)
    text = text.replace("’", "'").replace("‘", "'")
    text = text.lower()
    result = re.sub(r"\s*\b(mrt|station)\b.*|\s*\(opening.*?\)", "", text).strip()
    return result


def transform_df(df: pd.DataFrame) -> pd.DataFrame:

    filtered_df = df.loc[pd.col("rail_type") == "Mrt"]

    names_map = {
        "Harbourfront": "HarbourFront",
        "Macpherson": "MacPherson",
        "Garden By The Bay": "Gardens by the Bay",
        "One North": "one-north",
        "River Valley": "Fort Canning",
        "Ns6": "Sungei Kadut",
        "De2": "Sungei Kadut",
    }

    filtered_df["name"] = filtered_df["name"].replace(names_map, regex=True)

    unique_df = filtered_df.drop_duplicates(subset=["name"], ignore_index=True)

    station_name_df = unique_df.loc[:, ["name"]]

    return station_name_df


def sort_result(item: Place) -> int:
    return PRIMARY_TYPES.get(item.primary_type, 10)


async def fetch_coords(
    session: aiohttp.ClientSession, name: str, url: str
) -> list[float]:
    result = [np.nan, np.nan]
    if name == "Hillview":
        query = "500G Upper Bukit Timah Rd, Hillview, Singapore 678107"
    elif name == "Clementi":
        query = "3150 Commonwealth Ave W, Clementi, Singapore 129580"
    elif name == "Riviera":
        query = f"{name} MRT Station CP3"
    elif name == "Serangoon North":
        query = f"{name} MRT Station CR9"
    elif name:
        query = f"{name} MRT Station"
    else:
        return result

    body = {
        "textQuery": query,
        "languageCode": "en",
        "regionCode": "SG",
        "locationBias": {
            "rectangle": {
                "low": {"latitude": 1.1496, "longitude": 103.594},
                "high": {"latitude": 1.4784, "longitude": 104.0945},
            }
        },
    }

    try:
        async with session.post(url, json=body) as response:
            data = await response.json()

            if not data or not data.get("places"):
                return result

            validated = Places.model_validate(data)

    except aiohttp.ClientError:
        return result

    for place in sorted(validated.places, key=sort_result):
        if place.primary_type is not None and place.primary_type not in set(
            PRIMARY_TYPES
        ):
            continue

        if normalize_name(place.display_name.text) == normalize_name(name):
            result = [place.location.latitude, place.location.longitude]

            return result

    return result


async def fetch_all_coords(
    df: pd.DataFrame, headers: dict[str, str], url: str
) -> list[list[float]]:
    async with aiohttp.ClientSession(headers=headers) as session:
        tasks = [
            fetch_coords(session, row.name, url) for row in df.itertuples(index=False)
        ]
        results = await asyncio.gather(*tasks)

        return results


async def main() -> None:
    dataset_id = "d_2c06c9fe8ae724b5d33efa1f203e2c38"
    limiter = AsyncLimiter(2, 10)

    async with aiohttp.ClientSession(headers=HEADERS_DATA_GOV_SG) as session:
        config = APIConfig(session, limiter)
        data = await fetch_geo_data(config, dataset_id)
        adapter = TypeAdapter(list[Mrt])
        validated = adapter.validate_python(
            [feature["properties"] for feature in data["features"]]
        )

        raw_df = pd.DataFrame(adapter.dump_python(validated))

    df = transform_df(raw_df)

    coords = await fetch_all_coords(df, HEADERS_GOOGLE_MAPS, GOOGLE_MAPS_PLACES_URL)

    coords_df = add_coords(df, coords)

    data_dir = get_data_path()

    save_to_csv(coords_df, "mrt", data_dir)


if __name__ == "__main__":
    asyncio.run(main())
