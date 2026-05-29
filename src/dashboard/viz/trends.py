import pandas as pd
import plotly.graph_objects as go

from dashboard.viz.theme import (
    HOVER_LABEL_FONT,
    NEUTRAL_COLOR,
    PRIMARY_BASE_COLOR,
    PRIMARY_TINT_COLOR,
    TICK_FONT,
)


def build_monthly_median_price_line_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["month"],
            y=df["median_price"],
            mode="lines+markers",
            line=dict(color=PRIMARY_BASE_COLOR, width=2, shape="spline", smoothing=1),
            marker=dict(
                size=6,
                color=NEUTRAL_COLOR,
                line=dict(color=PRIMARY_BASE_COLOR, width=2),
            ),
            hovertemplate=(
                "<b>Month:</b> %{x}<br><b>Median Price:</b> $%{y:,.0f}<br><extra></extra>"
            ),
        )
    )

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
            tickformat="~s",  # e.g. 880k, 900k
        ),
    )

    return fig


def build_historical_median_price_line_chart(df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=df["year"],
            y=df["median_price"],
            mode="lines+markers",
            line=dict(color=PRIMARY_BASE_COLOR, width=2, shape="spline", smoothing=1),
            marker=dict(
                size=6,
                color="#ffffff",
                line=dict(color=PRIMARY_BASE_COLOR, width=2),
            ),
            hovertemplate=(
                "<b>Year:</b> %{x}<br><b>Median Price:</b> $%{y:,.0f}<br><extra></extra>"
            ),
        )
    )

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
