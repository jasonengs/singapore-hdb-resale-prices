from functools import cache

import numpy as np
import pandas as pd

from core.path import get_data_path


def cast_to_category(df: pd.DataFrame) -> None:
    cat_cols = [
        "town",
        "flat_type",
        "street_name",
        "flat_model",
        "full_address",
        "pln_area",
        "region",
        "nearest_station",
    ]

    df[cat_cols] = df[cat_cols].astype("category")


def cast_to_float(df: pd.DataFrame) -> None:
    df["remaining_lease"] = pd.to_numeric(df["remaining_lease"])


def cast_to_int(df: pd.DataFrame) -> None:
    int_cols = [
        "lease_commence_date",
        "year",
        "quarter",
        "month",
        "storey_lower",
        "storey_upper",
        "station_count",
    ]
    int_type = ["int8", "int16", "int32", "int64"]

    for col in int_cols:
        max_value = df[col].max()
        for dtype in int_type:
            if max_value <= np.iinfo(dtype).max:
                df[col] = df[col].astype(dtype)
                break
        else:
            df[col] = df[col].astype("int64")


@cache
def load_data() -> pd.DataFrame:
    df = pd.read_parquet(get_data_path() / "latest_data.parquet")
    # cast to float
    cast_to_float(df)
    # cast from string to category
    cast_to_category(df)
    # cast to optimal int
    cast_to_int(df)

    return df


@cache
def load_address() -> pd.DataFrame:
    df = pd.read_csv(get_data_path() / "address.csv")

    return df


@cache
def load_mrt() -> pd.DataFrame:
    df = pd.read_csv(get_data_path() / "mrt.csv")

    return df
