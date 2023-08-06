from __future__ import annotations

from typing import Dict

from pydantic import BaseModel
from pydantic import Field
from pydantic import root_validator


def pythonize(value):
    result = ''
    last_capital = False
    for char in value:
        if char.isupper():
            if not last_capital:
                result += '_'
            result += char.lower()
            last_capital = True
        else:
            result += char
            last_capital = False
    return result


class Row(BaseModel):
    key: str
    new_key_name: str = Field(default='')
    value: float | int | str | None
    of_type: str = Field(default='')

    @root_validator(pre=True)
    @classmethod
    def before(cls, values):
        values['of_type'] = type(values['value']).__name__
        values['new_key_name'] = pythonize(values['key'])
        return values

    def __repr__(self):
        if self.key == self.new_key_name:
            return f'{self.key}: {self.of_type}'
        else:
            return f"{self.new_key_name}: {self.of_type} = Field(alias='{self.key}')"


def parse_to_model(obj: Dict):
    return [Row(key=k, value=v) for k, v in obj.items()]


def create_model(name: str, obj: Dict):
    rows = parse_to_model(obj)
    print(f'class {name}(BaseModel):')
    for row in rows:
        print(f'    {row.__repr__()}')
