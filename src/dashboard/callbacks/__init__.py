from dashboard.callbacks.comparison import register_comparison_callbacks
from dashboard.callbacks.correlation import register_correlation_callbacks
from dashboard.callbacks.distribution import register_distribution_callbacks
from dashboard.callbacks.kpis import register_kpis_callbacks
from dashboard.callbacks.maps import register_maps_callbacks
from dashboard.callbacks.ranking import register_ranking_callbacks
from dashboard.callbacks.trends import register_trends_callbacks


def register_callbacks() -> None:
    register_kpis_callbacks()
    register_trends_callbacks()
    register_distribution_callbacks()
    register_correlation_callbacks()
    register_ranking_callbacks()
    register_comparison_callbacks()
    register_maps_callbacks()
