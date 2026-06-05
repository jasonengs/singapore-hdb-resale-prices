import pandas as pd
from dash import dcc, html


def create_global_dropdown(df: pd.DataFrame, category: str) -> dcc.Dropdown:
    unique_options = sorted(df[category].unique())

    options = [{"label": option, "value": option} for option in unique_options]

    value = df[category].max() if category == "year" else None

    clearable = False if category == "year" else True

    placeholder = (
        None if category == "year" else f"All {category.replace('_', ' ').title()}s"
    )

    dropdown = dcc.Dropdown(
        id=f"{category.replace('_', '-')}-dropdown",
        options=options,
        value=value,
        clearable=clearable,
        placeholder=placeholder,
    )

    return dropdown


def create_local_dropdown(
    id: str, options: list, value: str, label: str
) -> dcc.Dropdown:

    dropdown = html.Div(
        className="flex items-center gap-1.5",
        children=[
            html.Span(label, className="text-xs whitespace-nowrap text-gray-400"),
            dcc.Dropdown(
                id=id,
                options=[
                    {"label": option.title(), "value": option.replace(" ", "_")}
                    for option in options
                ],
                value=value.replace(" ", "_") or options[0].replace(" ", "_"),
                clearable=False,
                searchable=False,
            ),
        ],
    )

    return dropdown
