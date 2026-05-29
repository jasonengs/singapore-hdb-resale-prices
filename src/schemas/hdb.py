from pydantic import Field

from schemas.base import AppModel, CleanStr, MrtStr


class Mrt(AppModel):
    name: MrtStr = Field(..., alias="NAME")
    rail_type: MrtStr = Field(..., alias="RAIL_TYPE")


class Flat(AppModel):
    date: CleanStr = Field(..., alias="month")
    town: CleanStr
    flat_type: CleanStr
    block: CleanStr
    street_name: CleanStr
    storey_range: CleanStr
    floor_area_sqm: float
    flat_model: CleanStr
    lease_commence_date: int
    remaining_lease: CleanStr | None = None
    resale_price: float


class PriceIndex(AppModel):
    quarter: CleanStr
    index: float
