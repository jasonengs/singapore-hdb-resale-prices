import plotly.graph_objects as go


def get_empty_figure() -> go.Figure:
    fig = go.Figure()

    fig.add_annotation(
        text="No data found for the selected filters!",
        font=dict(color="#00a6f4", family="Roboto, sans serif", size=30, weight=500),
        # opacity=0.8,s
    )

    fig.update_layout(
        paper_bgcolor="#ffffff",
        plot_bgcolor="#ffffff",
        xaxis={
            "showgrid": False,
            "showticklabels": False,
            "showline": False,
            "zeroline": False,
        },
        yaxis={
            "showgrid": False,
            "showticklabels": False,
            "showline": False,
            "zeroline": False,
        },
    )

    return fig


def normalize_text(text: str) -> str:
    text = "planning area" if text == "pln_area" else text
    text = text.replace("_", " ").strip().title()

    return text


def get_hover_suffix_scatter(metric: str) -> str:
    if metric == "floor_area_sqm":
        suffix = " sqm"
    elif metric == "remaining_lease":
        suffix = " yrs"
    elif metric == "radius_km":
        suffix = " km"

    return suffix


def get_hover_title_scatter(metric: str) -> str:
    if metric == "floor_area_sqm":
        title = "Floor Area"
    else:
        title = normalize_text(metric)

    return title


def get_hover_pre_suffix(measure: str) -> str:
    pre_suffix = "" if measure == "transaction_count" else "$"

    return pre_suffix


def get_hover_suffix(measure: str) -> str:
    suffix = ":,.2f" if measure == "median_price_per_sqm" else ":,.0f"

    return suffix
