from collections.abc import Hashable

import pandas as pd
import plotly.graph_objects as go

from dashboard.viz.theme import HOVER_LABEL_FONT, NEUTRAL_COLOR, TICK_FONT


def build_town_ranking_bar(
    processed_df: pd.DataFrame,
    measure: Hashable,
    color: str,
    hovertemplate: str,
    order: str,
) -> go.Figure:

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=processed_df[measure],
            y=processed_df["town"],
            orientation="h",
            marker=dict(color=color, cornerradius=5),
            width=0.6,
            hovertemplate=hovertemplate,
        )
    )

    fig.update_layout(
        paper_bgcolor=NEUTRAL_COLOR,
        plot_bgcolor=NEUTRAL_COLOR,
        margin=dict(l=15, r=15, t=15, b=15),
        font=dict(family="Roboto, sans-serif", color="#6a7282"),
        bargap=0.4,
        hoverlabel=dict(
            bgcolor=NEUTRAL_COLOR,
            bordercolor="#d1d5dc",
            font=HOVER_LABEL_FONT,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            tickfont=TICK_FONT,
            tickformat="~s",
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            categoryorder=f"total {order}",
            tickfont=TICK_FONT,
            ticklabelstandoff=5,
        ),
    )

    return fig
