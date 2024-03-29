from __future__ import annotations

from enum import Enum, IntEnum, StrEnum
from typing import Any, NoReturn


class ConstantsMeta(type):
    def __setattr__(self, attr: str, nv: Any) -> NoReturn:
        raise RuntimeError(f"Constant <{attr}> cannot be assigned to.")

    def __delattr__(self, attr: str) -> NoReturn:
        raise RuntimeError(f"Constant <{attr}> cannot be deleted.")


class STRING(StrEnum):
    VERSION = "0.4.1"
