import plotly.graph_objects as go
from dash import Input, Output, callback

from dashboard.datasets.loader import load_data_cloud
from dashboard.transforms.aggregations import aggregate_df
from dashboard.transforms.enrichment import fill_missing_months
from dashboard.transforms.filters import filter_by_dropdowns, filter_by_year
from dashboard.viz.figure import get_empty_figure
from dashboard.viz.trends import (
    build_historical_median_price_line_chart,
    build_monthly_median_price_line_chart,
)


def register_trends_callbacks() -> None:

    @callback(
        Output("median-price-trend-monthly-line", "figure"),
        Input("year-dropdown", "value"),
        Input("town-dropdown", "value"),
        Input("flat-type-dropdown", "value"),
    )
    def update_monthly_median_price_line_chart(
        selected_year: int,
        selected_town: str | None,
        selected_flat_type: str | None,
    ) -> go.Figure:

        df = load_data_cloud()

        processed_df = (
            df.pipe(filter_by_year, selected_year)
            .pipe(filter_by_dropdowns, None, selected_town, selected_flat_type)
            .pipe(aggregate_df, "month", "resale_price", "median", "median_price")
        )

        if processed_df.empty:
            fig = get_empty_figure()
            return fig

        merged_df = fill_missing_months(processed_df)

        fig = build_monthly_median_price_line_chart(merged_df)

        return fig

    @callback(
        Output("median-price-trend-yearly-line", "figure"),
        Input("quarter-dropdown", "value"),
        Input("town-dropdown", "value"),
        Input("flat-type-dropdown", "value"),
    )
    def update_historical_median_price_line_chart(
        selected_quarter: int | None,
        selected_town: str | None,
        selected_flat_type: str | None,
    ) -> go.Figure:

        df = load_data_cloud()

        processed_df = df.pipe(
            filter_by_dropdowns, selected_quarter, selected_town, selected_flat_type
        ).pipe(aggregate_df, "year", "resale_price", "median", "median_price")

        if processed_df.empty:
            fig = get_empty_figure()
            return fig

        fig = build_historical_median_price_line_chart(processed_df)

        return fig
