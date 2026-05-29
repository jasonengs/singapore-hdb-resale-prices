import numbers


def abbreviate_number(value: int) -> str:
    if value >= 1000000:
        result = f"{value / 1000000:.3g}M"
    elif value >= 10000:
        result = f"{value / 1000:.0f}k"
    else:
        result = f"{value:,.0f}"
    return result


def format_metric_and_pct_change(
    metric: int | float | str,
    pct_change: int | float | str,
    currency: bool = False,
    metric_decimals: int = 0,
    pct_change_decimals: int = 1,
) -> tuple[str, str]:
    if isinstance(metric, (numbers.Number)):
        prefix = "$" if currency else ""
        metric_str = f"{prefix}{metric:,.{metric_decimals}f}"
    else:
        metric_str = metric

    if isinstance(pct_change, (numbers.Number)):
        pct_change_str = f"{abs(pct_change):,.{pct_change_decimals}f}%"
    else:
        pct_change_str = pct_change

    return metric_str, pct_change_str
