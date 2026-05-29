from typing import TypeVar

import pandas as pd
from pydantic import TypeAdapter

from schemas.hdb import Flat, PriceIndex

T = TypeVar("T", Flat, PriceIndex)


def to_dataframe(records: list[dict], model: type[T]) -> pd.DataFrame:
    adapter = TypeAdapter(list[model])
    validated = adapter.validate_python(records)

    df = pd.DataFrame(adapter.dump_python(validated))

    return df


def parse_date(df: pd.DataFrame) -> pd.DataFrame:
    # Cast date to datetime datatype
    df["date"] = pd.to_datetime(df["date"], format="%Y-%m")

    return df


def add_coords(df: pd.DataFrame, coords: list[list[float]]) -> pd.DataFrame:
    df[["lat", "lng"]] = pd.DataFrame(coords, index=df.index).round(6)

    return df
