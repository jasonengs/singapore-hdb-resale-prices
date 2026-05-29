from pydantic import Field

from schemas.base import AppModel


class Location(AppModel):
    latitude: float
    longitude: float


class DisplayName(AppModel):
    text: str


class Place(AppModel):
    location: Location
    display_name: DisplayName = Field(..., alias="displayName")
    primary_type: str | None = Field(None, alias="primaryType")


class Places(AppModel):
    places: list[Place]


class GeocodingLocation(AppModel):
    lat: float
    lng: float


class Geometry(AppModel):
    location: GeocodingLocation
