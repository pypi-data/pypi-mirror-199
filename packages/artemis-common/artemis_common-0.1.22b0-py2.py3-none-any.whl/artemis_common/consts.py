from __future__ import annotations

from enum import Enum

from pydantic import BaseSettings
from pydantic import Field
from pydantic import SecretStr


class Environment:
    KEY = 'ARTEMIS_ENV'
    DEV = DEFAULT = 'dev'
    PROD = 'prod'


LOGSENE_KEY = 'logsene-app-token'
ARTEMIS_DAL_API_KEY_NAME = 'x-artemis-dal-api-key'


class ArtemisEnvironment(BaseSettings):
    artemis_env: str = 'dev'


artemis_env = ArtemisEnvironment().artemis_env


class _EnvironmentVariables(BaseSettings):
    artemis_dal_api_key: SecretStr = Field(
        ...,
        env=f'{artemis_env}_ARTEMIS_DAL_API_KEY',
    )
