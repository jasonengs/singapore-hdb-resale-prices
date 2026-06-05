import plotly.graph_objects as go
from dash import Input, Output, callback

from dashboard.datasets.loader import (
    load_address_cloud,
    load_data_cloud,
    load_geojson_cloud,
    load_mrt_cloud,
)
from dashboard.transforms.aggregations import add_pct_change, aggregated_by_measure
from dashboard.transforms.enrichment import (
    assign_color,
    assign_trend,
    encode_pct_change,
)
from dashboard.transforms.filters import filter_by_dropdowns, filter_by_year
from dashboard.viz.figure import get_hover_pre_suffix, get_hover_suffix, normalize_text
from dashboard.viz.maps import (
    build_address_level_resale_activity_scatter_map,
    build_resale_market_choropleth_map,
)


def register_maps_callbacks() -> None:

    @callback(
        Output("resale-market-choropleth-map", "figure"),
        Input("year-dropdown", "value"),
        Input("quarter-dropdown", "value"),
        Input("flat-type-dropdown", "value"),
        Input("resale-market-geographic-dropdown", "value"),
        Input("resale-market-measure-dropdown", "value"),
    )
    def update_resale_market_choropleth_map(
        selected_year: int,
        selected_quarter: int | None,
        selected_flat_type: str | None,
        selected_geographic: str,
        measure: str,
    ) -> go.Figure:

        df = load_data_cloud()

        geographic = "pln_area" if selected_geographic == "planning_area" else "region"

        geojson = load_geojson_cloud(geographic)

        processed_df = (
            df.pipe(filter_by_year, selected_year, True)
            .pipe(filter_by_dropdowns, selected_quarter, None, selected_flat_type)
            .pipe(aggregated_by_measure, ["year", geographic], measure)
            .pipe(add_pct_change, ["year", geographic], measure)
            .pipe(filter_by_year, selected_year, False)
            .pipe(assign_color)
            .pipe(assign_trend)
            .pipe(encode_pct_change)
        )

        pre_suffix_hover = get_hover_pre_suffix(measure)
        suffix_hover = get_hover_suffix(measure)

        hovertemplate = (
            f"<b>{normalize_text(geographic)}:</b> %{{text}}<br>"
            f"<b>{normalize_text(measure)}:</b> {pre_suffix_hover}%{{z{suffix_hover}}}<br>"
            "<b>YoY Change:</b> <span style='color:%{customdata[1]}'> %{customdata[2]}%{customdata[0]}</span><br>"
            "<extra></extra>"
        )

        fig = build_resale_market_choropleth_map(
            processed_df, geojson, geographic, measure, hovertemplate
        )

        return fig

    @callback(
        Output("address-level-resale-activity-scatter-map", "figure"),
        Input("year-dropdown", "value"),
        Input("quarter-dropdown", "value"),
        Input("town-dropdown", "value"),
        Input("flat-type-dropdown", "value"),
        Input("address-level-resale-activity-measure-dropdown", "value"),
    )
    def update_address_level_resale_activity_scatter_map(
        selected_year: int,
        selected_quarter: int | None,
        selected_town: str | None,
        selected_flat_type: str | None,
        measure: str,
    ) -> go.Figure:

        df = load_data_cloud()
        mrt_df = load_mrt_cloud()
        address_df = load_address_cloud()

        processed_df = (
            df.pipe(filter_by_year, selected_year)
            .pipe(
                filter_by_dropdowns, selected_quarter, selected_town, selected_flat_type
            )
            .pipe(aggregated_by_measure, "full_address", measure)
            .merge(address_df, how="inner", on="full_address")
        )

        pre_suffix_hover = get_hover_pre_suffix(measure)
        suffix_hover = get_hover_suffix(measure)

        hovertemplate = (
            "<b>Address:</b> %{customdata[0]}<br>"
            f"<b>{normalize_text(measure)}:</b> {pre_suffix_hover}%{{customdata[1]{suffix_hover}}}<br>"
            "<extra></extra>"
        )

        fig = build_address_level_resale_activity_scatter_map(
            processed_df, mrt_df, measure, hovertemplate
        )

        return fig
