import plotly.graph_objects as go
from dash import Input, Output, callback

from dashboard.datasets.loader import load_data
from dashboard.transforms.aggregations import aggregated_by_measure
from dashboard.transforms.filters import (
    filter_by_dropdowns,
    filter_by_year,
    sort_df,
)
from dashboard.viz.figure import (
    get_empty_figure,
    get_hover_pre_suffix,
    get_hover_suffix,
    normalize_text,
)
from dashboard.viz.ranking import build_town_ranking_bar


def register_ranking_callbacks() -> None:

    @callback(
        Output("town-ranking-bar", "figure"),
        Input("year-dropdown", "value"),
        Input("quarter-dropdown", "value"),
        Input("flat-type-dropdown", "value"),
        Input("town-ranking-sort-dropdown", "value"),
        Input("town-ranking-measure-dropdown", "value"),
    )
    def update_town_ranking_bar(
        selected_year: int,
        selected_quarter: int | None,
        selected_flat_type: str | None,
        sort_order: str,
        measure: str,
    ) -> go.Figure:

        df = load_data()

        processed_df = (
            df.pipe(filter_by_year, selected_year)
            .pipe(filter_by_dropdowns, selected_quarter, None, selected_flat_type)
            .pipe(aggregated_by_measure, "town", measure)
            .pipe(sort_df, measure, sort_order)
        )

        if processed_df.empty:
            fig = get_empty_figure()
            return fig

        order = "ascending" if sort_order == "highest" else "descending"

        highlight = (
            processed_df[measure].max()
            if sort_order == "highest"
            else processed_df[measure].min()
        )

        color = [
            "#00a6f4" if row[measure] == highlight else "#74d4ff"
            for _, row in processed_df.iterrows()
        ]
        pre_suffix_hover = get_hover_pre_suffix(measure)
        suffix_hover = get_hover_suffix(measure)
        hovertemplate = (
            f"<b>Town:</b> %{{y}}<br>"
            f"<b>{normalize_text(measure)}:</b> {pre_suffix_hover}%{{x{suffix_hover}}}<br>"
            "<extra></extra>"
        )

        fig = build_town_ranking_bar(processed_df, measure, color, hovertemplate, order)

        return fig
