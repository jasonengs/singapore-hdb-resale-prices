from collections.abc import Hashable

import pandas as pd
from dash import Input, Output, callback

from dashboard.datasets.loader import load_data
from dashboard.metrics.formatters import format_metric_and_pct_change
from dashboard.metrics.lookup import get_metric_with_pct_change
from dashboard.models.kpis import DashboardKpis, KpiResult
from dashboard.transforms.aggregations import add_pct_change, aggregate_df
from dashboard.transforms.filters import filter_by_dropdowns, filter_by_year
from dashboard.viz.styles import get_badge_and_icon_classes


def register_kpis_callbacks() -> None:

    @callback(
        # median price
        Output("median-price-metric", "children"),
        Output("median-price-pct-change-metric", "children"),
        Output("median-price-pct-change-icon", "className"),
        Output("median-price-pct-change-badge", "className"),
        # total transaction
        Output("total-transaction-metric", "children"),
        Output("total-transaction-pct-change-metric", "children"),
        Output("total-transaction-pct-change-icon", "className"),
        Output("total-transaction-pct-change-badge", "className"),
        # median price per sqm
        Output("median-price-per-sqm-metric", "children"),
        Output("median-price-per-sqm-pct-change-metric", "children"),
        Output("median-price-per-sqm-pct-change-icon", "className"),
        Output("median-price-per-sqm-pct-change-badge", "className"),
        # median lease
        Output("median-lease-metric", "children"),
        Output("median-lease-pct-change-metric", "children"),
        Output("median-lease-pct-change-icon", "className"),
        Output("median-lease-pct-change-badge", "className"),
        Input("year-dropdown", "value"),
        Input("quarter-dropdown", "value"),
        Input("town-dropdown", "value"),
        Input("flat-type-dropdown", "value"),
    )
    def update_kpis(
        selected_year: int,
        selected_quarter: int | None,
        selected_town: str | None,
        selected_flat_type: str | None,
    ) -> DashboardKpis:
        df = load_data()

        filtered_year_df = df.pipe(filter_by_year, selected_year, True).pipe(
            filter_by_dropdowns, selected_quarter, selected_town, selected_flat_type
        )

        median_price_df = filtered_year_df.pipe(
            aggregate_df, "year", "resale_price", "median", "median_price"
        ).pipe(add_pct_change, "median_price")
        total_transaction_df = filtered_year_df.pipe(
            aggregate_df, "year", "resale_price", "count", "total_transaction"
        ).pipe(add_pct_change, "total_transaction")
        median_price_per_sqm_df = filtered_year_df.pipe(
            aggregate_df, "year", "price_per_sqm", "median", "median_price_per_sqm"
        ).pipe(add_pct_change, "median_price_per_sqm")
        median_lease_df = filtered_year_df.pipe(
            aggregate_df, "year", "remaining_lease", "median", "median_lease"
        ).pipe(add_pct_change, "median_lease")

        def render_kpi(
            kpi_df: pd.DataFrame,
            col: Hashable,
            currency: bool,
            metric_decimals: int = 0,
        ) -> KpiResult:
            metric, pct_change = get_metric_with_pct_change(
                kpi_df,
                selected_year,
                col,
            )
            metric_str, pct_change_str = format_metric_and_pct_change(
                metric, pct_change, currency=currency, metric_decimals=metric_decimals
            )
            badge, icon = get_badge_and_icon_classes(pct_change)

            return metric_str, pct_change_str, icon, badge

        kpis = (
            *render_kpi(median_price_df, "median_price", True, 0),
            *render_kpi(total_transaction_df, "total_transaction", False, 0),
            *render_kpi(median_price_per_sqm_df, "median_price_per_sqm", True, 2),
            *render_kpi(median_lease_df, "median_lease", False, 0),
        )

        return kpis
