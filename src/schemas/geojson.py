from typing import Annotated, Generic, Literal, TypeVar

from pydantic import Field

from schemas.base import (
    AppModel,
    RegionStr,
    TitleCaseStr,
)

Position = list[float]

PolygonCoords = list[list[Position]]

MultiPolygonCoords = list[list[list[Position]]]


class PolygonGeometry(AppModel):
    type: Literal["Polygon"]
    coordinates: PolygonCoords


class MultiPolygonGeometry(AppModel):
    type: Literal["MultiPolygon"]
    coordinates: MultiPolygonCoords


class RegionProperty(AppModel):
    region: RegionStr = Field(..., alias="REGION_N")


class PlnAreaProperty(RegionProperty):
    pln_area: TitleCaseStr = Field(..., alias="PLN_AREA_N")


Geometry = Annotated[
    PolygonGeometry | MultiPolygonGeometry, Field(discriminator="type")
]


class PlnAreaFeature(AppModel):
    type: Literal["Feature"]
    geometry: Geometry
    properties: PlnAreaProperty


class RegionFeature(AppModel):
    type: Literal["Feature"]
    geometry: Geometry
    properties: RegionProperty


F = TypeVar("F")


class FeatureCollection(AppModel, Generic[F]):
    type: Literal["FeatureCollection"]
    features: list[F]


class PlnAreaFeatureCollection(FeatureCollection[PlnAreaFeature]):
    pass


class RegionFeatureCollection(FeatureCollection[RegionFeature]):
    pass
