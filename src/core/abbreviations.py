import re

import pandas as pd

from core.constants import STREET_NAME_ABB


def get_key_length(item: tuple[str, str]) -> int:
    abbreviation = item[0]
    key_length = len(abbreviation)

    return key_length


def sort_by_key_length(abb_dict: dict[str, str]) -> dict[str, str]:
    sorted_dict = dict(sorted(abb_dict.items(), key=get_key_length, reverse=True))

    return sorted_dict


def make_pattern(abb_dict: dict) -> re.Pattern:
    escaped_keys = [re.escape(keys) for keys in abb_dict]

    alternatives = "|".join(escaped_keys)

    pattern_str = rf"(?<!\w)({alternatives})(?!\w)"

    compiled_pattern = re.compile(pattern_str)

    return compiled_pattern


def lowercase_after_apostrophe(match: re.Match) -> str:
    result = "'" + match.group(1).lower()

    return result


def clean_street_name(df: pd.DataFrame) -> pd.DataFrame:
    sorted_abb = sort_by_key_length(STREET_NAME_ABB)
    pattern = make_pattern(sorted_abb)

    def replace_match(match: re.Match) -> str:
        matched_text = match.group(0)
        expanded_form = sorted_abb[matched_text]

        return expanded_form

    df["street_name"] = df["street_name"].str.replace(
        pattern, replace_match, regex=True
    )
    # Convert the next character after "'" to lowercase
    df["street_name"] = df["street_name"].str.replace(
        r"'([A-Z]+)", lowercase_after_apostrophe, regex=True
    )

    df["street_name"] = df["street_name"].str.replace("Macpherson", "MacPherson")

    return df
