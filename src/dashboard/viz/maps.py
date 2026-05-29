from collections.abc import Hashable

import pandas as pd
import plotly.graph_objects as go

from dashboard.viz.theme import COLOR_SCALE, HOVER_LABEL_FONT, NEUTRAL_COLOR


def build_resale_market_choropleth_map(
    processed_df: pd.DataFrame,
    geojson: dict,
    geographic: Hashable,
    measure: Hashable,
    hovertemplate: str,
) -> go.Figure:

    fig = go.Figure(
        go.Choroplethmap(
            geojson=geojson,
            locations=processed_df[geographic],
            z=processed_df[measure],
            featureidkey=f"properties.{geographic}",
            colorscale=COLOR_SCALE,
            zmin=processed_df[measure].min(),
            zmax=processed_df[measure].max(),
            marker=dict(line=dict(color="white", width=1), opacity=0.85),
            colorbar=dict(
                outlinecolor="#101828",
                outlinewidth=1,
                thickness=15,
                tickfont=dict(size=11),
                tickformat="~s",
            ),
            text=processed_df[geographic],
            customdata=processed_df.iloc[:, 3:],
            hovertemplate=hovertemplate,
        )
    )

    fig.update_layout(
        paper_bgcolor=NEUTRAL_COLOR,
        plot_bgcolor=NEUTRAL_COLOR,
        margin={"r": 15, "t": 15, "l": 15, "b": 15},
        font=dict(family="Roboto, sans-serif", color="#6a7282"),
        hoverlabel=dict(
            bgcolor=NEUTRAL_COLOR,
            bordercolor="#d1d5dc",
            font=dict(size=13, color="#101828"),
        ),
        map=dict(
            style="carto-positron", zoom=10, center=dict(lat=1.3521, lon=103.8198)
        ),
    )

    return fig


def build_address_level_resale_activity_scatter_map(
    processed_df: pd.DataFrame,
    mrt_df: pd.DataFrame,
    measure: Hashable,
    hovertemplate: str,
) -> go.Figure:
    fig = go.Figure()

    fig.add_trace(
        go.Scattermap(
            lat=processed_df["lat"],
            lon=processed_df["lng"],
            mode="markers",
            marker=dict(
                size=20,
                opacity=0.5,
                colorscale=COLOR_SCALE,
                cmin=processed_df[measure].min(),
                color=processed_df[measure],
                cmax=processed_df[measure].max(),
            ),
            customdata=processed_df.iloc[:, :2],
            hovertemplate=hovertemplate,
        )
    )

    fig.add_trace(
        go.Scattermap(
            lat=mrt_df["lat"],
            lon=mrt_df["lng"],
            mode="markers",
            marker=dict(size=10, color="black", symbol="rail"),
            text=mrt_df["name"],
            hovertemplate="<b>MRT:</b> %{text}<br><extra></extra>",
        )
    )

    fig.update_layout(
        paper_bgcolor=NEUTRAL_COLOR,
        plot_bgcolor=NEUTRAL_COLOR,
        margin={"r": 15, "t": 15, "l": 15, "b": 15},
        font=dict(family="Roboto, sans-serif", color="#6a7282"),
        hoverlabel=dict(
            bgcolor=NEUTRAL_COLOR,
            bordercolor="#d1d5dc",
            font=HOVER_LABEL_FONT,
        ),
        showlegend=False,
        map=dict(
            style="carto-positron", zoom=10, center=dict(lat=1.3521, lon=103.8198)
        ),
    )

    return fig
