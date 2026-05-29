import os
from dataclasses import dataclass

from aiohttp import ClientSession
from aiolimiter import AsyncLimiter
from dotenv import find_dotenv, load_dotenv


@dataclass(frozen=True)
class APIConfig:
    session: ClientSession
    limiter: AsyncLimiter


load_dotenv(find_dotenv(), override=True)


DATA_GOV_SG_API_KEY = os.getenv("DATA_GOV_SG_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")

HEADERS_DATA_GOV_SG = {"x-api-key": DATA_GOV_SG_API_KEY}

HEADERS_GOOGLE_MAPS = {
    "Content-Type": "application/json",
    "X-Goog-Api-Key": GOOGLE_MAPS_API_KEY,
    "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.location,places.primaryType,",
}
