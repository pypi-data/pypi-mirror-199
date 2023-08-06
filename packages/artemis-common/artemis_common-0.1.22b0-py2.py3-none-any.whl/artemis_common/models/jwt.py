from __future__ import annotations

from datetime import datetime

from .bases import AdvancedBaseModel


class APIKeyModel(AdvancedBaseModel):
    api_key: str


class JWTModel(AdvancedBaseModel):
    token: str


class JWTPayloadModel(AdvancedBaseModel):
    user_id: str
    api_key_hash: str


class JWTDecodedPayloadModel(JWTPayloadModel):
    iss: str
    exp: datetime
    iat: datetime


__all__ = [
    APIKeyModel.__name__,
    JWTModel.__name__,
    JWTPayloadModel.__name__,
    JWTDecodedPayloadModel.__name__,
]
