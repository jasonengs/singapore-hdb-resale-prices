from dash import html

from dashboard.components.cards import create_chart_card, create_kpi_card
from dashboard.components.dropdowns import create_global_dropdown, create_local_dropdown
from dashboard.components.tables import create_ag_grid
from dashboard.datasets.loader import load_data_cloud


def create_layout() -> html.Div:
    df = load_data_cloud()

    div = html.Div(
        className="min-h-screen bg-gray-50 font-sans",
        children=[
            # 1 ── Sticky filter bar
            html.Header(
                className="sticky top-0 z-50 bg-white border-b border-gray-200 shadow-sm",
                children=[
                    html.Div(
                        className="flex items-center gap-4 px-5 py-2.5 flex-wrap",
                        children=[
                            html.Span(
                                "Singapore HDB Resale Prices",
                                className="text-sm font-bold text-gray-900 whitespace-nowrap mr-3",
                            ),
                            html.Div(
                                className="flex items-center gap-3 flex-wrap",
                                children=[
                                    html.Div(
                                        [
                                            html.Label(
                                                "Year",
                                                className="text-xs text-gray-400 whitespace-nowrap",
                                            ),
                                            create_global_dropdown(df, "year"),
                                        ],
                                        className="flex items-center gap-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Quarter",
                                                className="text-xs text-gray-400 whitespace-nowrap",
                                            ),
                                            create_global_dropdown(df, "quarter"),
                                        ],
                                        className="flex items-center gap-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Town",
                                                className="text-xs text-gray-400 whitespace-nowrap",
                                            ),
                                            create_global_dropdown(df, "town"),
                                        ],
                                        className="flex items-center gap-2",
                                    ),
                                    html.Div(
                                        [
                                            html.Label(
                                                "Flat Type",
                                                className="text-xs text-gray-400 whitespace-nowrap",
                                            ),
                                            create_global_dropdown(df, "flat_type"),
                                        ],
                                        className="flex items-center gap-2",
                                    ),
                                ],
                            ),
                        ],
                    )
                ],
            ),
            html.Main(
                className="p-5 flex flex-col gap-5",
                children=[
                    # 2a ── KPI Cards
                    html.Div(
                        className="grid grid-cols-4 gap-4",
                        children=[
                            create_kpi_card(
                                "Median Price",
                                "median-price-metric",
                                "median-price-pct-change-badge",
                                "median-price-pct-change-icon",
                                "median-price-pct-change-metric",
                            ),
                            create_kpi_card(
                                "Total Transaction",
                                "total-transaction-metric",
                                "total-transaction-pct-change-badge",
                                "total-transaction-pct-change-icon",
                                "total-transaction-pct-change-metric",
                            ),
                            create_kpi_card(
                                "Median Price/sqm",
                                "median-price-per-sqm-metric",
                                "median-price-per-sqm-pct-change-badge",
                                "median-price-per-sqm-pct-change-icon",
                                "median-price-per-sqm-pct-change-metric",
                            ),
                            create_kpi_card(
                                "Median Lease",
                                "median-lease-metric",
                                "median-lease-pct-change-badge",
                                "median-lease-pct-change-icon",
                                "median-lease-pct-change-metric",
                            ),
                        ],
                    ),
                    # 2b --- Monthly price trend + Historical price trend
                    html.Div(
                        className="grid grid-cols-2 gap-4",
                        children=[
                            create_chart_card(
                                "Monthly Price Trend",
                                subtitle="Median resale price by month",
                                graph_id="median-price-trend-monthly-line",
                            ),
                            create_chart_card(
                                "Historical Price Trend",
                                subtitle="Annual median resale price from 1990 to present",
                                graph_id="median-price-trend-yearly-line",
                            ),
                        ],
                    ),
                    # 2c --- Resale distribution by flat type + Resale price correlation
                    html.Div(
                        className="grid grid-cols-2 gap-4",
                        children=[
                            create_chart_card(
                                "Resale Price Distribution by Flat Type",
                                controls=[
                                    create_local_dropdown(
                                        "resale-price-distribution-type-dropdown",
                                        ["median price", "price distribution"],
                                        "median price",
                                        "Chart type:",
                                    )
                                ],
                                graph_id="resale-price-distribution-bar-box",
                            ),
                            create_chart_card(
                                "Resale Price Correlation",
                                controls=[
                                    create_local_dropdown(
                                        "resale-price-correlation-metric-dropdown",
                                        [
                                            "floor area sqm",
                                            "remaining lease",
                                            "radius km",
                                        ],
                                        "floor area sqm",
                                        "Compare with:",
                                    )
                                ],
                                graph_id="resale-price-correlation-scatter",
                            ),
                        ],
                    ),
                    # 2d --- Town ranking + Year-on-Year regional performance
                    html.Div(
                        className="grid grid-cols-2 gap-4",
                        children=[
                            create_chart_card(
                                "Town Ranking",
                                controls=[
                                    create_local_dropdown(
                                        "town-ranking-sort-dropdown",
                                        ["highest", "lowest"],
                                        "highest",
                                        "Rank By:",
                                    ),
                                    create_local_dropdown(
                                        "town-ranking-measure-dropdown",
                                        [
                                            "median price",
                                            "transaction count",
                                            "median price per sqm",
                                        ],
                                        "median price",
                                        "Measure:",
                                    ),
                                ],
                                graph_id="town-ranking-bar",
                            ),
                            create_chart_card(
                                "Year-on-Year Regional Performance",
                                controls=[
                                    create_local_dropdown(
                                        "year-on-year-regional-measure-dropdown",
                                        [
                                            "median price",
                                            "transaction count",
                                            "median price per sqm",
                                        ],
                                        "median price",
                                        "Measure:",
                                    )
                                ],
                                graph_id="year-on-year-regional-butterfly-chart",
                            ),
                        ],
                    ),
                    # 2e --- Resale market heatmap + Address-level resale activity
                    html.Div(
                        className="grid grid-cols-2 gap-4",
                        children=[
                            create_chart_card(
                                "Resale Market Heatmap",
                                controls=[
                                    create_local_dropdown(
                                        "resale-market-geographic-dropdown",
                                        ["region", "planning area"],
                                        "region",
                                        "Filter By:",
                                    ),
                                    create_local_dropdown(
                                        "resale-market-measure-dropdown",
                                        [
                                            "median price",
                                            "transaction count",
                                            "median price per sqm",
                                        ],
                                        "median price",
                                        "Measure:",
                                    ),
                                ],
                                graph_id="resale-market-choropleth-map",
                            ),
                            create_chart_card(
                                "Address-Level Resale Activity",
                                controls=[
                                    create_local_dropdown(
                                        "address-level-resale-activity-measure-dropdown",
                                        [
                                            "median price",
                                            "transaction count",
                                            "median price per sqm",
                                        ],
                                        "median price",
                                        "Measure:",
                                    )
                                ],
                                graph_id="address-level-resale-activity-scatter-map",
                            ),
                        ],
                    ),
                    # 2f --- Recent resale transactions
                    html.Div(
                        className="bg-white border border-gray-200 rounded-xl overflow-hidden",
                        children=[
                            html.Div(
                                className="px-4 pt-4 pb-3 border-b border-gray-100",
                                children=[
                                    html.Span(
                                        "Recent Resale Transactions",
                                        className="text-sm font-semibold text-gray-800",
                                    )
                                ],
                            ),
                            html.Div(className="p-1", children=create_ag_grid(df)),
                        ],
                    ),
                ],
            ),
        ],
    )
    return div
