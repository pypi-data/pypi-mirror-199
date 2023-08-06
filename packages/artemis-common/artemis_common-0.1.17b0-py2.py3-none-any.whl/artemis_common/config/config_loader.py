from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Type

from pydantic import BaseModel
from pydantic import ValidationError


class ConfigFileLoadError(Exception):
    pass


class ConfigLoader:
    def __init__(
        self,
        config_file_path: Path,
        config_model: Type[BaseModel],
    ) -> None:
        self._config_file_path = config_file_path
        self._config_model = config_model
        self._config = None

    @property
    def config(self) -> Type[BaseModel]:
        if self._config:
            return self._config
        self._config = self._load_config()
        self._setup_logging()
        return self._config

    def _load_config(self) -> Type[BaseModel]:
        try:
            raw_config = self._config_file_path.read_text()
            json_config = json.loads(raw_config)
            return self._config_model(**json_config)
        except OSError as ex:
            raise ConfigFileLoadError('Config file was not found!') from ex
        except ValidationError as ex:
            raise ConfigFileLoadError('Config file does not match the given model') from ex
        except ValueError as ex:
            raise ConfigFileLoadError('Config file is not a valid json!') from ex

    def _setup_logging(self):
        logging.config.dictConfig(self._config.logging)
