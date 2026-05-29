from typing import Annotated

from pydantic import BaseModel, BeforeValidator, ConfigDict


def strip_text(v: object) -> object:
    return v.strip() if isinstance(v, str) else v


def transform_to_title_case(v: object) -> object:
    return v.title() if isinstance(v, str) else v


def clean_region(v: object) -> object:
    return v.replace("REGION", "") if isinstance(v, str) else v


def clean_mrt(v: object) -> object:
    return v.replace("INTERCHANGE", "") if isinstance(v, str) else v


class AppModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True, extra="ignore")


CleanStr = Annotated[
    str, BeforeValidator(strip_text), BeforeValidator(transform_to_title_case)
]
TitleCaseStr = Annotated[
    str, BeforeValidator(strip_text), BeforeValidator(transform_to_title_case)
]
RegionStr = Annotated[
    str,
    BeforeValidator(strip_text),
    BeforeValidator(transform_to_title_case),
    BeforeValidator(clean_region),
]

MrtStr = Annotated[
    str,
    BeforeValidator(strip_text),
    BeforeValidator(transform_to_title_case),
    BeforeValidator(clean_mrt),
]
