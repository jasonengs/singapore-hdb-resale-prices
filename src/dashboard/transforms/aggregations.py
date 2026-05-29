from collections.abc import Callable, Hashable

import pandas as pd


def aggregate_df(
    df: pd.DataFrame,
    groupby_cols: str | list[str],
    agg_cols: Hashable | list[Hashable],
    agg_funcs: Callable | list[Callable],
    col_names: Hashable | list[Hashable],
) -> pd.DataFrame:
    # Normalize to lists if single values are passed
    if not isinstance(agg_cols, list):
        agg_cols, agg_funcs, col_names = [agg_cols], [agg_funcs], [col_names]

    aggregations = {
        col_name: (agg_col, agg_func)
        for col_name, agg_col, agg_func in zip(col_names, agg_cols, agg_funcs)
    }

    agg_df = df.groupby(groupby_cols, as_index=False).aggregate(**aggregations)

    return agg_df


def aggregated_by_measure(
    df: pd.DataFrame, groupby_col: Hashable | list[Hashable], measure: str
) -> pd.DataFrame:

    if measure == "median_price":
        agg_df = aggregate_df(df, groupby_col, "resale_price", "median", measure)
    elif measure == "transaction_count":
        agg_df = aggregate_df(df, groupby_col, "resale_price", "count", measure)
    elif measure == "median_price_per_sqm":
        agg_df = aggregate_df(df, groupby_col, "price_per_sqm", "median", measure)

    return agg_df


def add_pct_change(
    df: pd.DataFrame,
    col_name: Hashable | list[Hashable],
    agg_col: Hashable | None = None,
) -> pd.DataFrame:
    if not isinstance(col_name, list):
        df["pct_change"] = df[col_name].pct_change() * 100
    else:
        sort_col, groupby_col = col_name

        df = df.sort_values(by=sort_col, ignore_index=True)

        df["pct_change"] = df.groupby(groupby_col)[agg_col].pct_change() * 100

    return df
