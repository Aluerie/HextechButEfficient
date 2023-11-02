from __future__ import annotations

import logging
from contextlib import contextmanager
from logging.handlers import RotatingFileHandler
from pathlib import Path

__all__ = ("setup_logging",)


@contextmanager
def setup_logging(debug: bool = False):
    log = logging.getLogger()
    if debug:
        log.setLevel(logging.DEBUG)
    else:
        log.setLevel(logging.INFO)

    try:
        formatter = logging.Formatter(
            "{asctime} | {levelname:<7} | {funcName:<30} | {message}",
            "%H:%M:%S %d/%m",
            style="{",
        )

        # Stream Handler
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        log.addHandler(handler)

        # ensure temp/logs folders folder
        Path(".logs/").mkdir(parents=True, exist_ok=True)
        # File Handler
        file_handler = RotatingFileHandler(
            filename=f".logs/hextech.log",
            encoding="utf-8",
            mode="w",
            maxBytes=16 * 1024 * 1024,  # 16 MiB
            backupCount=1,  # Rotate through 1 files
        )
        file_handler.setFormatter(formatter)
        log.addHandler(file_handler)
        yield
    finally:
        # __exit__
        handlers = log.handlers[:]
        for hdlr in handlers:
            hdlr.close()
            log.removeHandler(hdlr)
