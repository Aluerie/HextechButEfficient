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


class NotLoggedIn(CustomException):
    """User is not logged in.

    Sometimes the LCU API is ready but looks like user is not YET logged in, so we need to raise this.
    Also can happen when league is dead.
    """

    __slots__: tuple[str, ...] = ()
