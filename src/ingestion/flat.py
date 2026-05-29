import asyncio
from datetime import datetime

import aiohttp
import pandas as pd
from aiolimiter import AsyncLimiter

from core.api import fetch_dataset_id, fetch_latest_data
from core.config import HEADERS_DATA_GOV_SG, APIConfig
from core.path import get_data_path
from core.save import save_to_csv
from core.transform import parse_date, to_dataframe
from schemas.hdb import Flat


def build_filename(df: pd.DataFrame) -> str:
    parsed_df = parse_date(df)
    # Get min year from date column
    min_year = parsed_df["date"].min().year
    # Get max year from date column
    max_year = parsed_df["date"].max().year
    # Define the filename
    filename = f"flat_prices_{min_year}_to_{max_year}"
    return filename


async def main() -> None:
    limiter = AsyncLimiter(8, 15)  # 8 request per 15 seconds
    # # Get data path
    data_dir = get_data_path()
    # Get the current year
    current_year = datetime.today().year
    async with aiohttp.ClientSession(headers=HEADERS_DATA_GOV_SG) as session:
        config = APIConfig(session, limiter)

        # Get dataset id from API
        datasets_id = await fetch_dataset_id(config)
        # # find all existing flat_prices CSV files and sorted the newest first
        files = sorted(list(data_dir.glob("flat_prices_*_to_*.csv")), reverse=True)

        if files:
            # Get the most recent file
            latest_file = files[0]
            # Extract ending year from filename
            latest_file_year = int(latest_file.stem.split("_")[-1])

            # if the latest file is from the current year, update it
            if latest_file_year == current_year:
                # Update current year data
                records = await fetch_latest_data(config, datasets_id[0])
                # Convert records into dataframe
                df = to_dataframe(records, Flat)
                filename = build_filename(df)
                save_to_csv(df, filename, data_dir)
            # if the latest file is outdated, delete and fetch
            elif latest_file_year < current_year:
                # Remove outdated files
                latest_file.unlink(missing_ok=True)
                # Fetch and save data for the current year
                records = await fetch_latest_data(config, datasets_id[0])
                # Convert records into dataframe
                df = to_dataframe(records, Flat)
                filename = build_filename(df)
                save_to_csv(df, filename, data_dir)
        else:
            tasks = [
                fetch_latest_data(config, dataset_id) for dataset_id in datasets_id
            ]

            pages = await asyncio.gather(*tasks)

            dfs = [to_dataframe(records, Flat) for records in pages]
            for df in dfs:
                filename = build_filename(df)
                save_to_csv(df, filename, data_dir)


if __name__ == "__main__":
    asyncio.run(main())
