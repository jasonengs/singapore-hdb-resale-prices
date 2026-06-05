import pandas as pd
import plotly.graph_objects as go
from dash import Input, Output, callback

from dashboard.datasets.loader import load_data_cloud
from dashboard.transforms.aggregations import add_pct_change, aggregated_by_measure
from dashboard.transforms.enrichment import assign_badge, encode_pct_change
from dashboard.transforms.filters import filter_by_dropdowns, filter_by_year
from dashboard.viz.comparison import build_year_on_year_regional_butterfly_chart
from dashboard.viz.figure import get_hover_pre_suffix, get_hover_suffix


def register_comparison_callbacks() -> None:

    @callback(
        Output("year-on-year-regional-butterfly-chart", "figure"),
        Input("year-dropdown", "value"),
        Input("quarter-dropdown", "value"),
        Input("flat-type-dropdown", "value"),
        Input("year-on-year-regional-measure-dropdown", "value"),
    )
    def update_year_on_year_regional_butterfly_chart(
        selected_year: int,
        selected_quarter: int | None,
        selected_flat_type: str | None,
        measure: str,
    ) -> go.Figure:

        df = load_data_cloud()

        processed_df = (
            df.pipe(filter_by_year, selected_year, True)
            .pipe(filter_by_dropdowns, selected_quarter, None, selected_flat_type)
            .pipe(aggregated_by_measure, ["year", "region"], measure)
            .pipe(add_pct_change, ["year", "region"], measure)
            .pipe(assign_badge)
            .pipe(encode_pct_change)
            .sort_values(
                by=["year", measure, "pct_change"], ascending=[True, True, True]
            )
        )

        pre_suffix_hover = get_hover_pre_suffix(measure)
        suffix_hover = get_hover_suffix(measure)

        cy_df = processed_df.loc[pd.col("year") == selected_year]
        py_df = processed_df.loc[pd.col("year") == (selected_year - 1)]

        fig = build_year_on_year_regional_butterfly_chart(
            py_df, cy_df, measure, selected_year, pre_suffix_hover, suffix_hover
        )

        return fig
