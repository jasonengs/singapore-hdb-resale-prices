from typing import NamedTuple


class KpiResult(NamedTuple):
    metric: str
    pct_change: str
    icon: str
    badge: str


class DashboardKpis(NamedTuple):
    median_price: KpiResult
    total_transaction: KpiResult
    median_price_per_sqm: KpiResult
    median_lease: KpiResult
