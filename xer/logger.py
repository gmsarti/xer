"""Logger configuration for the Xer project.

The logger is configured based on the values defined in :class:`xer.config.Settings`.
It respects the ``log_level`` and ``log_file`` settings, falling back to a sensible
default when those values are not provided.
"""

import logging
from pathlib import Path
from typing import Optional

from .config import get_settings

def _ensure_log_dir(path: Path) -> None:
    """Create the directory for the log file if it does not exist.

    The function is safe to call multiple times – ``mkdir`` with ``exist_ok=True``
    will not raise an error if the directory already exists.
    """
    if not path.parent.exists():
        path.parent.mkdir(parents=True, exist_ok=True)

def configure_logger() -> logging.Logger:
    """Configure and return a module‑level logger.

    The logger name is ``"xer"`` so that it can be easily filtered in larger
    applications.  It is configured with a ``StreamHandler`` (stdout) and, when a
    ``log_file`` is defined, a ``FileHandler`` that writes rotating logs.
    """
    settings = get_settings()
    logger = logging.getLogger("xer")
    logger.setLevel(settings.log_level.upper())
    # Avoid adding duplicate handlers if this function is called multiple times
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # Optional file handler
    log_file: Optional[str] = getattr(settings, "log_file", None)
    if log_file:
        log_path = Path(log_file).expanduser().resolve()
        _ensure_log_dir(log_path)
        file_handler = logging.FileHandler(log_path, encoding="utf-8")
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    logger.propagate = False
    return logger

# Expose a ready‑to‑use logger instance for the rest of the codebase
logger = configure_logger()
