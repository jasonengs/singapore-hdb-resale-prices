import pandas as pd
import plotly.graph_objects as go

from dashboard.transforms.aggregations import aggregate_df
from dashboard.viz.theme import (
    HOVER_LABEL_FONT,
    NEUTRAL_COLOR,
    PRIMARY_BASE_COLOR,
    PRIMARY_TINT_COLOR,
    TICK_FONT,
)


def build_resale_price_distribution_bar_box(
    processed_df: pd.DataFrame, chart_type: str
) -> go.Figure:

    fig = go.Figure()

    if chart_type == "median_price":
        agg_df = aggregate_df(
            processed_df, "flat_type", "resale_price", "median", "median_price"
        )

        fig.add_trace(
            go.Bar(
                x=agg_df["flat_type"],
                y=agg_df["median_price"],
                marker=dict(
                    color=PRIMARY_BASE_COLOR,
                    cornerradius=5,
                ),
                width=0.6,
                hovertemplate=(
                    "<b>Flat Type:</b> %{x}<br><b>Median Price:</b> $%{y:,.0f}<br><extra></extra>"
                ),
            )
        )

        fig.update_layout(
            bargap=0.4,
        )

    elif chart_type == "price_distribution":
        fig.add_trace(
            go.Box(
                x=processed_df["flat_type"],
                y=processed_df["resale_price"],
                marker=dict(
                    color=PRIMARY_BASE_COLOR,
                    # size=3,
                    line=dict(outliercolor=PRIMARY_BASE_COLOR),
                ),
                width=0.6,
                line=dict(color=PRIMARY_BASE_COLOR, width=1.5),
                fillcolor=PRIMARY_TINT_COLOR,
            )
        )

        fig.update_layout(boxgap=0.4, yaxis=dict(hoverformat=",.0f"))

    fig.update_layout(
        paper_bgcolor=NEUTRAL_COLOR,
        plot_bgcolor=NEUTRAL_COLOR,
        margin=dict(l=15, r=15, t=15, b=15),
        font=dict(family="Roboto, sans-serif", color="#6a7282"),
        hoverlabel=dict(
            bgcolor=NEUTRAL_COLOR,
            bordercolor=PRIMARY_TINT_COLOR,
            font=HOVER_LABEL_FONT,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=TICK_FONT,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=TICK_FONT,
            tickformat="~s",
        ),
    )

    return fig
