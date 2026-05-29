def get_badge_and_icon_classes(
    pct: int | float | str,
) -> tuple[str, str]:
    if isinstance(pct, str) or pct == 0:
        badge_class = "inline-flex items-center gap-1 rounded-md bg-gray-100 px-2 py-0.5 text-xs font-semibold text-gray-500"
        icon_class = "fa-solid fa-minus text-xs"
    elif pct > 0:
        badge_class = "inline-flex items-center gap-1 rounded-md bg-emerald-100 px-2 py-0.5 text-xs font-semibold text-emerald-700"
        icon_class = "fa-solid fa-arrow-trend-up text-xs"
    elif pct < 0:
        badge_class = "inline-flex items-center gap-1 rounded-md bg-rose-100 px-2 py-0.5 text-xs font-semibold text-rose-700"
        icon_class = "fa-solid fa-arrow-trend-down text-xs"

    return badge_class, icon_class
