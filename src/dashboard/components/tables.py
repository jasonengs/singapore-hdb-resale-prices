import pandas as pd
from dash_ag_grid import AgGrid

from dashboard.transforms.filters import filter_by_year


def create_ag_grid(df: pd.DataFrame) -> AgGrid:
    filtered_df = filter_by_year(df, df["year"].max(), True).sort_values(
        by=["year", "month", "town"], ascending=[False, False, True], ignore_index=False
    )
    filtered_df["date"] = filtered_df["date"].dt.strftime("%Y-%m")

    filtered_df.columns = [column.replace("_", " ") for column in filtered_df.columns]

    columnsDefs = [
        {"field": "date", "width": 140},
        {"field": "town"},
        {"field": "block", "width": 140},
        {"field": "street name"},
        {"field": "flat type", "width": "180", "cellRenderer": "flatTypeBadge"},
        {"field": "nearest station"},
        {
            "field": "radius km",
            "width": "150",
            "type": "numericColumn",
        },
        {
            "field": "remaining lease",
            "width": 180,
            "type": "numericColumn",
            "valueFormatter": {"function": "params.value + ' yrs'"},
        },
        {
            "field": "floor area sqm",
            "headerName": "Floor Area",
            "width": "150",
            "type": "numericColumn",
            "valueFormatter": {"function": "params.value + ' sqm'"},
        },
        {
            "field": "resale price",
            "width": 160,
            "type": "numericColumn",
            "valueFormatter": {"function": "d3.format('$,.0f')(params.value)"},
        },
    ]

    ag_grid = AgGrid(
        id="singapore-resale-ag-grid",
        className="ag-theme-singapore",
        rowData=filtered_df.to_dict("records"),
        rowClassRules={
            "row-even": "params.node.rowIndex % 2 === 0",
            "row-odd": "params.node.rowIndex % 2 !== 0",
        },
        columnDefs=columnsDefs,
        columnSize="sizeToFit",
        defaultColDef={
            "sortable": True,
            "filter": True,
            "resizable": False,
            "suppressMovable": True,
            "floatingFilter": True,
        },
        dashGridOptions={
            "pagination": True,
            "paginationPageSize": 20,
            "paginationPageSizeSelector": [10, 20, 50, 100],
            "animateRows": True,
            "rowHeight": 44,
            "headerHeight": 46,
            "floatingFiltersHeight": 38,
            "domLayout": "normal",
            "suppressCellFocus": False,
            "enableCellTextSelection": True,
        },
        style={"height": "570px", "width": "100%"},
    )

    return ag_grid
