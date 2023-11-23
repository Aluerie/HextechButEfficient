from __future__ import annotations

import logging

log = logging.getLogger(__name__)


__all__: tuple[str, ...] = (
    "CustomException",
    "ConfirmationDenied",
)


class CustomException(Exception):
    """The base exception for this project. All other custom-made exceptions should inherit from this."""

    __slots__: tuple[str, ...] = ()


class ConfirmationDenied(CustomException):
    """Confirmation was not received."""

    __slots__: tuple[str, ...] = ()
