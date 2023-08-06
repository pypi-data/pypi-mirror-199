from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import Field
from pydantic import root_validator

from artemis_common.models.bases import AdvancedBaseModel
from artemis_common.models.bases import ValueBaseModel


class CategoryModel(AdvancedBaseModel):
    id: int
    name: str


class SerieModel(AdvancedBaseModel):
    id: str
    realtime_start: datetime
    realtime_end: datetime
    title: str
    observation_start: datetime
    observation_end: datetime
    frequency: str
    frequency_short: str
    units: str
    units_short: str
    seasonal_adjustment: str
    seasonal_adjustment_short: str
    last_updated: datetime
    last_updated_date: datetime
    popularity: int
    group_popularity: int
    notes: Optional[str]
    active: bool


class ObservationModel(AdvancedBaseModel):
    observations: list[ValueBaseModel]

    @root_validator(pre=True)
    def validate_values(cls, values):
        observations = values['observations']
        values['observations'] = [
            obs for obs in observations
            if obs['value'] != '.'
        ]
        return values


__all__ = [
    CategoryModel.__name__,
    SerieModel.__name__,
    ObservationModel.__name__,
]
