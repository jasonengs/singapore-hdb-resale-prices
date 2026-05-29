import asyncio

import aiohttp
import pandas as pd
from aiolimiter import AsyncLimiter

from core.api import fetch_latest_data
from core.config import HEADERS_DATA_GOV_SG, APIConfig
from core.path import get_data_path
from core.save import save_to_csv
from core.transform import to_dataframe
from schemas.hdb import PriceIndex


def transform_df(df: pd.DataFrame) -> pd.DataFrame:
    # Create year and quarter column based on quarter column after splitting
    df[["year", "quarter"]] = df["quarter"].str.split("-", expand=True)
    # Remove "Q" and cast to int
    df["quarter"] = df["quarter"].str.replace("Q", "").astype("int")
    final_df = df.loc[:, ["year", "quarter", "index"]]

    return final_df


async def main():
    limiter = AsyncLimiter(8, 10)

    datasets_id = "d_14f63e595975691e7c24a27ae4c07c79"
    # Create a session
    async with aiohttp.ClientSession(headers=HEADERS_DATA_GOV_SG) as session:
        config = APIConfig(session, limiter)
        # Get data
        records = await fetch_latest_data(config, datasets_id)

    # Convert it into dataframe
    df = to_dataframe(records, PriceIndex)

    final_df = transform_df(df)
    # Get data path
    data_dir = get_data_path()
    # Define filename
    filename = "resale_price_index"
    # Save dataframe to csv
    save_to_csv(final_df, filename, data_dir)


if __name__ == "__main__":
    asyncio.run(main())
