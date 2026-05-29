from dash import dcc, html


def create_kpi_card(
    title: str, metric_id: str, badge_id: str, icon_id: str, pct_id: str
) -> html.Div:
    card = html.Div(
        className="flex flex-col gap-3 rounded-xl border border-l-4 border-gray-300 border-l-sky-500 bg-white p-4 shadow-sm hover:shadow-md hover:-translate-y-1 focus:outline-none focus:shadow-md focus:translate-y-[-4px] transition-all duration-200",
        children=[
            html.Div(
                className="flex items-center justify-between",
                children=[
                    html.Span(title, className="text-sm font-medium text-gray-500"),
                    html.Div(
                        id=badge_id,
                        className="inline-flex animate-pulse items-center gap-1 rounded-md bg-gray-200 px-2 py-0.5 text-xs font-semibold text-gray-500",
                        children=[
                            html.I(
                                id=icon_id,
                                className="h-3 w-5 animate-pulse rounded bg-gray-200",
                            ),
                            html.Span(
                                id=pct_id,
                                children="",
                            ),
                        ],
                    ),
                ],
            ),
            html.P(
                id=metric_id,
                className="text-2xl font-bold text-gray-900 tabular-nums",
                children=html.Div(
                    className=("h-7 w-28 animate-pulse rounded bg-gray-200")
                ),
            ),
        ],
    )

    return card


def create_chart_card(title, subtitle=None, controls=None, graph_id=None) -> html.Div:
    card_header = html.Div(
        className="flex flex-wrap items-center gap-2 border-b border-gray-100 px-4 pt-4 pb-3",
        children=[
            html.Span(title, className="text-sm font-semibold text-gray-800"),
            *(
                [html.Span(subtitle, className="ml-1 text-xs text-gray-400")]
                if subtitle
                else []
            ),
            *([html.Div(controls, className="ml-auto flex gap-2")] if controls else []),
        ],
    )

    card = html.Div(
        className="overflow-hidden rounded-xl border border-gray-200 bg-white shadow-sm hover:shadow-lg focus:outline-none focus:shadow-lg transition-all duration-200",
        children=[
            card_header,
            html.Div(
                children=[dcc.Graph(id=graph_id, config={"displayModeBar": False})],
                className="p-1",
            ),
        ],
    )

    return card
