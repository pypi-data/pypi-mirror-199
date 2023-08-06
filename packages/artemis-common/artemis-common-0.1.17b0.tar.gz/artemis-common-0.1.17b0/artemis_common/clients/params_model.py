from __future__ import annotations

from pydantic import BaseModel
from pydantic import Field


class ParamsModel(BaseModel):
    class Config:
        use_enum_values = True
        allow_population_by_field_name = True
        underscore_attrs_are_private = True


class DALParamsModel(ParamsModel):
    user_id: str = Field(default=None)
    category_id: int = Field(default=None, ge=0)
    gte: int = Field(default=None, ge=0, le=100)
    lte: int = Field(default=None, ge=0, le=100)
    serie_id: str = Field(default=None)

    def get_params(self):
        params_dict = self.dict(exclude_none=True, by_alias=True)
        return params_dict


__all__ = [
    DALParamsModel.__name__,
]
