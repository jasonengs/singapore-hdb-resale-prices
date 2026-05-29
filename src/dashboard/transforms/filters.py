from collections.abc import Hashable

import pandas as pd


def filter_df(
    df: pd.DataFrame, col: Hashable, value: str | int | float
) -> pd.DataFrame:
    filtered_df = df.loc[pd.col(col) == value]

    return filtered_df


def filter_by_year(
    df: pd.DataFrame, year: int, include_prev: bool = False
) -> pd.DataFrame:
    years = [year, year - 1] if include_prev else [year]

    filtered_df = df.loc[(pd.col("year").isin(years))]

    return filtered_df


def filter_by_dropdowns(
    df: pd.DataFrame, quarter: int | None, town: str | None, flat_type: str | None
) -> pd.DataFrame:
    filtered_df = df

    if quarter is not None:
        filtered_df = filter_df(filtered_df, "quarter", quarter)
    if town is not None:
        filtered_df = filter_df(filtered_df, "town", town)
    if flat_type is not None:
        filtered_df = filter_df(filtered_df, "flat_type", flat_type)

    return filtered_df


def sort_df(df: pd.DataFrame, measure: str, sort_order: str, n=5) -> pd.DataFrame:
    if sort_order == "highest":
        sorted_df = df.nlargest(n, measure)
    elif sort_order == "lowest":
        sorted_df = df.nsmallest(n, measure)

    return sorted_df
