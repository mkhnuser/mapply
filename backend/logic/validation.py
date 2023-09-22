# Ignore expression usage for type annotations.
# For example, constr, confloat, etc.
# type: ignore
from typing import Optional

from pydantic import BaseModel, confloat, constr, conint


# Use lower camel case for attribute names which contain two or more words.
# For example, mapEvents, userGroupPermissions, etc.


class PositionModel(BaseModel):
    lat: confloat(ge=-90, le=90, allow_inf_nan=False)
    lng: confloat(ge=-180, le=180, allow_inf_nan=False)


class MapEventModel(BaseModel):
    id: Optional[conint(ge=1)] = None
    title: constr(strip_whitespace=True, max_length=64)
    description: constr(strip_whitespace=True, max_length=512)
    position: PositionModel
