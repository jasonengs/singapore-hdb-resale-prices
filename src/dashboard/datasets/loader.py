import json
from functools import cache
from io import BytesIO

import geopandas as gpd
import numpy as np
import pandas as pd
from google.cloud import storage

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
def load_data_local() -> pd.DataFrame:
    df = pd.read_parquet(get_data_path() / "latest_data.parquet", engine="pyarrow")
    # cast to float
    cast_to_float(df)
    # cast from string to category
    cast_to_category(df)
    # cast to optimal int
    cast_to_int(df)

    return df


@cache
def load_address_local() -> pd.DataFrame:
    df = pd.read_csv(get_data_path() / "address.csv")

    return df


@cache
def load_mrt_local() -> pd.DataFrame:
    df = pd.read_csv(get_data_path() / "mrt.csv")

    return df


def load_bucket() -> storage.bucket.Bucket:
    client_storage = storage.Client()

    bucket = client_storage.bucket("sg-hdb-resale")

    return bucket


def load_blob_bytes(filename: str) -> BytesIO:
    blob = load_bucket().blob(f"data/{filename}")

    data = blob.download_as_bytes()

    results = BytesIO(data)

    return results


@cache
def load_data_cloud() -> pd.DataFrame:
    data = load_blob_bytes("latest_data.parquet")

    df = pd.read_parquet(data, engine="pyarrow")

    # cast to float
    cast_to_float(df)
    # cast from string to category
    cast_to_category(df)
    # cast to optimal int
    cast_to_int(df)

    return df


@cache
def load_address_cloud() -> pd.DataFrame:
    data = load_blob_bytes("address.csv")

    df = pd.read_csv(data)

    return df


@cache
def load_mrt_cloud() -> pd.DataFrame:
    data = load_blob_bytes("mrt.csv")

    df = pd.read_csv(data)

    return df


@cache
def load_gdf_cloud(layer: str) -> gpd.GeoDataFrame:
    data = load_blob_bytes(f"{layer}.geojson")

    gdf = gpd.read_file(data)

    return gdf


@cache
def load_geojson_cloud(layer: str) -> dict:
    gdf = load_gdf_cloud(layer)

    geojson = json.loads(gdf.to_json())

    return geojson
