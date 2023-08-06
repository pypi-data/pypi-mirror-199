from __future__ import annotations

from datetime import datetime
from typing import Optional

from dateutil.parser import parse
from pydantic import BaseModel
from pydantic import Extra
from pydantic import Field
from pydantic import root_validator


def parse_date_generic(date: str | datetime | int) -> datetime:
    if type(date) == datetime:
        return date.replace(tzinfo=None)

    if type(date) == int:
        return datetime.fromtimestamp(date)

    return parse(date).replace(tzinfo=None)


class AdvancedBaseModel(BaseModel):
    class Config:
        allow_population_by_field_name = True

    @root_validator(pre=True)
    def dates_parser(cls, values):
        scheme = cls.schema()
        properties = scheme['properties']
        for prop, settings in properties.items():
            if prop in values and \
                    settings.get('type') == 'string' and \
                    settings.get('format') == 'date-time':
                values[prop] = parse_date_generic(values[prop])
        return values


class DateBaseModel(AdvancedBaseModel):
    date: datetime


class ValueBaseModel(DateBaseModel):
    value: float


class CountBaseModel(AdvancedBaseModel):
    count: int
