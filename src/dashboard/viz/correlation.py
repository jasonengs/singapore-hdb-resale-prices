from collections.abc import Hashable

import pandas as pd
import plotly.graph_objects as go

from dashboard.viz.theme import (
    FLAT_TYPE_COLORS,
    HOVER_LABEL_FONT,
    NEUTRAL_COLOR,
    TICK_FONT,
)


def build_resale_price_correlation_scatter(
    processed_df: pd.DataFrame,
    flat_types: list,
    x_metric: Hashable,
    suffix: str,
    hover_title: str,
) -> go.Figure:
    fig = go.Figure()

    for flat_type in flat_types:
        flat_type_df = processed_df.loc[pd.col("flat_type") == flat_type]

        fig.add_trace(
            go.Scattergl(
                x=flat_type_df[x_metric],
                y=flat_type_df["resale_price"],
                name=flat_type,
                mode="markers",
                marker=dict(
                    color=FLAT_TYPE_COLORS["flat_type"][flat_type]["color"]["tint"],
                    opacity=0.6,
                    size=10,
                    line=dict(
                        color=FLAT_TYPE_COLORS["flat_type"][flat_type]["color"]["base"],
                        width=1,
                    ),
                ),
                hovertemplate=(
                    f"<b>{hover_title}:</b> %{{x}}<br>"
                    f"<b>Resale Price:</b> $%{{y:,.0f}}<br>"
                    "<extra></extra>"
                ),
                hoverlabel=dict(
                    bordercolor=FLAT_TYPE_COLORS["flat_type"][flat_type]["color"][
                        "base"
                    ],
                ),
            )
        )

        fig.update_layout(
            xaxis=dict(ticksuffix=suffix),
        )

        fig.update_layout(
            paper_bgcolor=NEUTRAL_COLOR,
            plot_bgcolor=NEUTRAL_COLOR,
            margin=dict(l=15, r=15, t=50, b=15),
            font=dict(family="Roboto, sans-serif"),
            legend=dict(
                orientation="h",
                x=0.5,
                y=1.02,
                xanchor="center",
                yanchor="bottom",
                bgcolor="rgba(0,0,0,0)",  # transparent
                itemsizing="constant",
                tracegroupgap=0,
                font=dict(color="#4a5565"),
            ),
            hoverlabel=dict(
                bgcolor=NEUTRAL_COLOR,
                font=HOVER_LABEL_FONT,
            ),
            xaxis=dict(
                nticks=5,
                gridcolor="#f3f4f6",
                tickfont=TICK_FONT,
                showline=False,
                zeroline=False,
            ),
            yaxis=dict(
                gridcolor="#f3f4f6",
                tickfont=TICK_FONT,
                tickformat="~s",
                showline=False,
                zeroline=False,
            ),
        )

    return fig
