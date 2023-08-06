from __future__ import annotations

from .bases import AdvancedBaseModel


class APIKeyModel(AdvancedBaseModel):
    api_key: str


class JWTPayloadModel(AdvancedBaseModel):
    user_id: str
    api_key_hash: str


__all__ = [
    APIKeyModel.__name__,
    JWTPayloadModel.__name__,
]
