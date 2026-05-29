import asyncio
from pathlib import Path

import aiohttp
import pandas as pd
from aiolimiter import AsyncLimiter

from core.abbreviations import clean_street_name
from core.config import GOOGLE_MAPS_API_KEY
from core.constants import GOOGLE_MAPS_GEOCODING_URL
from core.path import get_data_path
from core.save import save_to_csv
from core.transform import add_coords
from schemas.google import Geometry

SEM = asyncio.Semaphore(5)


def load_data(path: Path) -> pd.DataFrame:
    files = list(path.glob("flat_price*_to_*.csv"))

    df = pd.concat(
        [pd.read_csv(file) for file in files],
        ignore_index=True,
    )

    return df


def build_full_address(df: pd.DataFrame) -> pd.DataFrame:
    # Create address column by concatenating block column with " " street name column and " Singapore"
    df["full_address"] = df["block"] + " " + df["street_name"] + ", Singapore"
    # Remove duplications
    final_df = df.loc[:, ["full_address"]].drop_duplicates(ignore_index=True)

    return final_df


def clean_full_address(df: pd.DataFrame) -> pd.DataFrame:
    # Remove ", Singapore"
    df["full_address"] = df["full_address"].str.replace(", Singapore", "").str.strip()

    return df


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    cleaned_df = df.pipe(clean_street_name).pipe(build_full_address)

    return cleaned_df


def process_and_save(df: pd.DataFrame, filename: str, path: Path) -> None:
    # Clean dataframe by removing ", Singapore"
    cleaned_df = clean_full_address(df)
    # Save to csv
    save_to_csv(cleaned_df, filename, path)


async def fetch_coords(
    session: aiohttp.ClientSession,
    limiter: AsyncLimiter,
    address: str,
    api_key: str,
    url: str,
) -> list[float]:
    params = {"address": address, "region": "sg", "key": api_key}
    async with SEM:
        async with limiter:
            async with session.get(url, params=params) as response:
                data = await response.json()

    geometry = data["results"][0]["geometry"]
    validated = Geometry.model_validate(geometry)
    coordinates = [validated.location.lat, validated.location.lng]

    return coordinates


async def fetch_all_coords(
    df: pd.DataFrame, api_key: str, url: str
) -> list[list[float]]:
    limiter = AsyncLimiter(20, 2)

    async with aiohttp.ClientSession() as session:
        tasks = [
            fetch_coords(session, limiter, row, api_key, url)
            for row in df["full_address"]
        ]

        results = await asyncio.gather(*tasks)

    return results


async def main() -> None:
    # Get data path
    data_dir = get_data_path()
    filename = "address"

    address_file = data_dir / f"{filename}.csv"

    # Check whether the file exist or not if yes then update the current data otherwise get the data
    if address_file.exists():
        # Load latest data
        files = list(data_dir.glob("flat_prices_2017_to_202*.csv"))
        df = pd.read_csv(files[0])
        # Clean street name column and remove duplication
        cleaned_df = prepare_data(df)
        # Load address data
        address_df = pd.read_csv(address_file)
        # Construct full_address columns by concatenating ", Singapore"
        address_df["full_address"] = address_df["full_address"] + ", Singapore"
        # Filter cleaned_df
        filtered_df = cleaned_df.loc[
            ~cleaned_df["full_address"].isin(address_df["full_address"])
        ]
        if not filtered_df.empty:
            # Fetch latitude and longitude
            coords = await fetch_all_coords(
                filtered_df, GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_GEOCODING_URL
            )
            coords_df = add_coords(df, coords)
            # Update address_df by combining cleaned_df
            final_df = pd.concat([address_df, coords_df]).drop_duplicates(
                subset=["full_address"]
            )
            process_and_save(final_df, filename, data_dir)
    else:
        # Load all the data
        df = load_data(data_dir)
        # Clean street name column and remove duplication
        cleaned_df = prepare_data(df)
        # Fetch latitude and longitude
        coords = await fetch_all_coords(
            cleaned_df, GOOGLE_MAPS_API_KEY, GOOGLE_MAPS_GEOCODING_URL
        )
        coords_df = add_coords(cleaned_df, coords)
        # Save data tp csv and geojson
        process_and_save(cleaned_df, filename, data_dir)


if __name__ == "__main__":
    asyncio.run(main())
