from collections.abc import Hashable

import pandas as pd


def get_scalar_by_year(
    df: pd.DataFrame, year: int, col_name: Hashable
) -> int | float | str:
    filtered_df = df.loc[pd.col("year") == year, col_name]

    result = filtered_df.iloc[-1] if not filtered_df.empty else None

    result = "No Data" if result is None or pd.isna(result) else result

    return result


def get_metric_with_pct_change(
    df: pd.DataFrame,
    year: int,
    col_name: Hashable,
) -> tuple[int | float | str, int | float | str]:

    metric = get_scalar_by_year(df, year, col_name)

    pct_change = get_scalar_by_year(df, year, "pct_change")

    return metric, pct_change
