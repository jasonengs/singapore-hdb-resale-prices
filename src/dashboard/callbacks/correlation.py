import plotly.graph_objects as go
from dash import Input, Output, callback

from dashboard.datasets.loader import load_data_cloud
from dashboard.transforms.filters import filter_by_dropdowns, filter_by_year
from dashboard.viz.correlation import build_resale_price_correlation_scatter
from dashboard.viz.figure import (
    get_empty_figure,
    get_hover_suffix_scatter,
    get_hover_title_scatter,
)


def register_correlation_callbacks() -> None:

    @callback(
        Output("resale-price-correlation-scatter", "figure"),
        Input("year-dropdown", "value"),
        Input("quarter-dropdown", "value"),
        Input("town-dropdown", "value"),
        Input("resale-price-correlation-metric-dropdown", "value"),
    )
    def update_resale_price_correlation_scatter(
        selected_year: int,
        selected_quarter: int | None,
        selected_town: str | None,
        x_metric: str,
    ) -> go.Figure:
        df = load_data_cloud()

        processed_df = (
            df.pipe(filter_by_year, selected_year)
            .pipe(filter_by_dropdowns, selected_quarter, selected_town, None)
            .sort_values(by=["flat_type"])
        )

        if processed_df.empty:
            fig = get_empty_figure()
            return fig

        suffix = get_hover_suffix_scatter(x_metric)
        hover_title = get_hover_title_scatter(x_metric)

        flat_types = sorted(processed_df["flat_type"].unique())

        fig = build_resale_price_correlation_scatter(
            processed_df, flat_types, x_metric, suffix, hover_title
        )

        return fig
