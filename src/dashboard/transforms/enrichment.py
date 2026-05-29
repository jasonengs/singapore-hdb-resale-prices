from collections.abc import Hashable

import numpy as np
import pandas as pd


def fill_missing_months(df: pd.DataFrame) -> pd.DataFrame:
    monthly_df = pd.DataFrame({"month": range(1, 13)})

    merged_df = monthly_df.merge(df, how="left", on="month")

    merged_df["month"] = pd.to_datetime(merged_df["month"], format="%m").dt.strftime(
        "%b"
    )

    return merged_df


def select_by_pct(
    df: pd.DataFrame, pct_col: Hashable, positive: str, negative: str, neutral: str
) -> np.ndarray:
    condition = [df[pct_col] > 0, df[pct_col] < 0]
    result = np.select(condition, [positive, negative], default=neutral)

    return result


def assign_color(df: pd.DataFrame, pct_col: Hashable = "pct_change") -> pd.DataFrame:
    df["color"] = select_by_pct(df, pct_col, "#00bc7d", "#ff2056", "#6a7282")

    return df


def assign_trend(df: pd.DataFrame, pct_col: Hashable = "pct_change") -> pd.DataFrame:
    df["trend"] = select_by_pct(df, pct_col, "▲", "▼", "◆")

    return df


def assign_badge(df: pd.DataFrame, pct_col: Hashable = "pct_change") -> pd.DataFrame:
    df["font_color"] = select_by_pct(df, pct_col, "#007a55", "#c70036", "#6a7282")
    df["bg_color"] = select_by_pct(df, pct_col, "#d0fae5", "#ffe4e6", "#f3f4f6")
    df["trend"] = select_by_pct(df, pct_col, "+", "-", "")

    return df


def encode_pct_change(
    df: pd.DataFrame, pct_col: Hashable = "pct_change"
) -> pd.DataFrame:
    df[pct_col] = np.where(
        pd.notna(df[pct_col]),
        df[pct_col].map("{:.2f}%".format),
        "No Data",
    )
    df[pct_col] = df[pct_col].str.replace("-", "")

    return df
