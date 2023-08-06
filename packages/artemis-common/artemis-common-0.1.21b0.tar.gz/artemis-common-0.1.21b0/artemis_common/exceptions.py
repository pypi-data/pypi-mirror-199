from __future__ import annotations

from typing import Optional


class ArtemisException(Exception):
    pass


class ArtemisOperationFailedError(ArtemisException):
    pass


class ArtemisOperationUnexpectedlyFailedError(ArtemisException):
    def __init__(self, message: Optional[str] = None):
        if not message:
            message = ''
        super().__init__(f'[Unexpected] {message}')


class ArtemisUnexpectedFlowError(ArtemisException):
    def __init__(self):
        super().__init__('[Unexpected] Should not reach this line of code!')
