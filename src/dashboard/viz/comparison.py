import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

from dashboard.metrics.formatters import abbreviate_number
from dashboard.viz.figure import normalize_text
from dashboard.viz.theme import (
    HOVER_LABEL_FONT,
    NEUTRAL_COLOR,
    PRIMARY_BASE_COLOR,
    PRIMARY_TINT_COLOR,
    SECONDARY_BASE_COLOR,
    SECONDARY_TINT_COLOR,
)


def build_year_on_year_regional_butterfly_chart(
    py_df: pd.DataFrame,
    cy_df: pd.DataFrame,
    measure: str,
    selected_year: int,
    pre_suffix_hover: str,
    suffix_hover: str,
) -> go.Figure:

    fig = make_subplots(
        rows=1,
        cols=3,
        column_widths=[0.44, 0.12, 0.44],
        horizontal_spacing=0,
    )

    # Previous year bars (left)
    fig.add_trace(
        go.Bar(
            x=-py_df[measure],
            y=py_df["region"],
            name=f"{selected_year - 1}",
            orientation="h",
            marker=dict(
                color=SECONDARY_BASE_COLOR,
                cornerradius=5,
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            width=0.6,
            text=py_df[measure].map(abbreviate_number),
            texttemplate=f"{pre_suffix_hover}%{{text}}",
            textposition="inside",
            textfont=dict(color=NEUTRAL_COLOR, size=10),
            customdata=py_df[measure],
            hovertemplate=(
                f"<b>Region:</b> %{{y}}<br><b>{normalize_text(measure)}:</b> {pre_suffix_hover}%{{customdata{suffix_hover}}}<extra></extra>"
            ),
            hoverlabel=dict(bordercolor=SECONDARY_TINT_COLOR),
        ),
        row=1,
        col=1,
    )

    # Center column: invisible placeholder bars
    fig.add_trace(
        go.Bar(
            x=[0] * len(cy_df),
            y=cy_df["region"],
            orientation="h",
            marker=dict(
                color="rgba(0,0,0,0)",
                line=dict(color="rgba(0,0,0,0)"),
            ),
            showlegend=False,
            hoverinfo="skip",
        ),
        row=1,
        col=2,
    )

    # Current year bars (right)
    fig.add_trace(
        go.Bar(
            x=cy_df[measure],
            y=cy_df["region"],
            name=f"{selected_year}",
            orientation="h",
            marker=dict(
                color=PRIMARY_BASE_COLOR,
                cornerradius=5,
                line=dict(color="rgba(0,0,0,0)", width=0),
            ),
            width=0.6,
            text=cy_df[measure].map(abbreviate_number),
            texttemplate=f"{pre_suffix_hover}%{{text}}",
            textposition="inside",
            textfont=dict(color=NEUTRAL_COLOR, size=10),
            hovertemplate=(
                f"<b>Region:</b> %{{y}}<br><b>{normalize_text(measure)}:</b> {pre_suffix_hover}%{{x{suffix_hover}}}<extra></extra>"
            ),
            hoverlabel=dict(bordercolor=PRIMARY_TINT_COLOR),
        ),
        row=1,
        col=3,
    )

    # Stacked annotations: region name (top) + pct change badge (bottom)
    for _, row in cy_df.iterrows():
        # Region name
        fig.add_annotation(
            xref="x2",
            yref="y2",
            x=0,
            y=row["region"],
            text=f"<b>{row['region']}</b>",
            showarrow=False,
            font=dict(size=11, color="#101828"),
            yshift=8,
        )
        # Pct change badge
        fig.add_annotation(
            xref="x2",
            yref="y2",
            x=0,
            y=row["region"],
            text=f"<b>{row['trend']}{row['pct_change']}</b>",
            showarrow=False,
            font=dict(size=10, color=row["font_color"]),
            bgcolor=row["bg_color"],
            yshift=-8,
        )

    # Layout
    fig.update_layout(
        paper_bgcolor=NEUTRAL_COLOR,
        plot_bgcolor=NEUTRAL_COLOR,
        margin=dict(l=15, r=15, t=50, b=15),
        font=dict(family="Roboto, sans-serif"),
        barmode="relative",
        bargap=0.4,
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
            bgcolor="#ffffff",
            font=HOVER_LABEL_FONT,
        ),
        xaxis=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False,
        ),
        xaxis2=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False,
        ),
        xaxis3=dict(
            showticklabels=False,
            showgrid=False,
            zeroline=False,
            showline=False,
        ),
        yaxis=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            visible=False,
        ),
        yaxis2=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            visible=False,
        ),
        yaxis3=dict(
            showgrid=False,
            zeroline=False,
            showline=False,
            visible=False,
        ),
    )

    return fig
