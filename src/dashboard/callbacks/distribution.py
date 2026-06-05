import plotly.graph_objects as go
from dash import Input, Output, callback

from dashboard.datasets.loader import load_data_cloud
from dashboard.transforms.filters import filter_by_dropdowns, filter_by_year
from dashboard.viz.distribution import build_resale_price_distribution_bar_box
from dashboard.viz.figure import get_empty_figure


def register_distribution_callbacks() -> None:

    @callback(
        Output("resale-price-distribution-bar-box", "figure"),
        Input("year-dropdown", "value"),
        Input("quarter-dropdown", "value"),
        Input("town-dropdown", "value"),
        Input("resale-price-distribution-type-dropdown", "value"),
    )
    def update_resale_price_distribution_bar_box(
        selected_year: int,
        selected_quarter: int | None,
        selected_town: str | None,
        chart_type: str,
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

        fig = build_resale_price_distribution_bar_box(processed_df, chart_type)

        return fig
