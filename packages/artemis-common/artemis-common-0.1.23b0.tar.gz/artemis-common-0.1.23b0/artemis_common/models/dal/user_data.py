from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel
from pydantic import Field

from artemis_common.models.bases import AdvancedBaseModel


class UserAPIKeyModel(AdvancedBaseModel):
    id: str
    salt: str
    api_key_hash: str
    creation_time: str


__all__ = [
    UserAPIKeyModel.__name__,
]
