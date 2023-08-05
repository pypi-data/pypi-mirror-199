"""Custom logging handlers."""

import logging
import os
from logging import FileHandler, LogRecord, StreamHandler

from rich.console import Console
from rich.text import Text


class RichConsoleHandler(StreamHandler):  # pyright: ignore[reportMissingTypeArgument]
    """Logging handler for rich console output."""

    def __init__(self) -> None:
        """Initialize rich console handler."""
        super().__init__()  # pyright: ignore[reportUnknownMemberType]

        self.console = Console()

    def emit(self, record: LogRecord) -> None:
        """Emit a rich formatted version of the record message."""
        try:
            self.console.print(self.format(record))
        except (KeyboardInterrupt, SystemExit):
            raise
        except Exception:
            self.handleError(record)


class RichFileHandler(FileHandler):
    """Logging handler for file output with stripped formatting."""

    def __init__(self, filename: str) -> None:
        """Initialize rich file handler."""
        super().__init__(filename)

    def emit(self, record: LogRecord) -> None:
        """Emit a plain-text version of the record message."""
        record.msg = Text.from_markup(str(record.msg)).plain
        return super().emit(record)


LOG_LEVEL = logging.DEBUG if os.getenv("RUN_MODE", "").lower() == "debug" else logging.INFO

log = logging.getLogger("main")
log.setLevel(LOG_LEVEL)


def debug(msg: str):
    """Log a debug message."""
    log.debug(f":information_source: {msg}")


def info(msg: str):
    """Log an info message."""
    log.info(f"{msg}")


def info_bold(msg: str):
    """Log an info message in bold."""
    log.info(f"[bold yellow]{msg}")


def warning(msg: str):
    """Log warning message."""
    log.warning(f":exclamation:[bold yellow]{msg}")


def error(msg: str):
    """Log error message."""
    log.error(f":x: [bold red]{msg}")
