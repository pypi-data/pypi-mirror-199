from __future__ import annotations

from pathlib import Path
from typing import Type

from pydantic import BaseModel

from .config_loader import ConfigLoader
from artemis_common.consts import artemis_env


def get_config(config_dir: Path, config_model: Type[BaseModel]) -> Type[BaseModel]:
    config_file_path = config_dir.joinpath('files', f'config_{artemis_env}.json')
    return ConfigLoader(config_file_path, config_model).config
