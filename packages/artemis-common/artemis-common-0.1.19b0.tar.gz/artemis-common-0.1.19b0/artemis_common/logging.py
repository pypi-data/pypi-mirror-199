from __future__ import annotations

import logging
from typing import Optional

from artemis_common.consts import LOGSENE_KEY


class SyslogAdapter(logging.LoggerAdapter):
    def process(self, msg: str, kwargs: dict):
        extra = kwargs.setdefault('extra', {})
        for key, value in self.extra.items():
            extra[key] = value
        return msg, kwargs


def get_logger(name: str, token: str, extra: Optional[dict] = None) -> SyslogAdapter:
    if not extra:
        extra = {}
    logger = logging.getLogger(name)
    return SyslogAdapter(
        logger,
        {LOGSENE_KEY: token, **extra},
    )
