"""Logging configuration for MissionForge."""

import logging
import sys
import warnings
from pathlib import Path

from rich.logging import RichHandler

# Suppress harmless hashlib blake2 errors from Python 3.12.3 OpenSSL builds
# These occur when OpenSSL doesn't have blake2 compiled in, but Python's
# built-in implementation is used as fallback (functionality is not affected)
logging.getLogger().addFilter(
    lambda record: not (
        record.levelno == logging.ERROR
        and "code for hash blake2" in record.getMessage()
    )
)


def setup_logging(
    level: str = "INFO", log_file: Path | None = None, rich_output: bool = True
) -> logging.Logger:
    """Configure logging with Rich handler.

    Args:
        level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        log_file: Optional file path for logging output.
        rich_output: Whether to use Rich formatting for console output.

    Returns:
        Configured logger instance.
    """
    logger = logging.getLogger("missionforge")
    logger.setLevel(level.upper())

    # Remove existing handlers to avoid duplicates
    logger.handlers.clear()

    # Console handler with Rich
    if rich_output:
        console_handler: logging.Handler = RichHandler(
            rich_tracebacks=True,
            markup=True,
            show_time=False,
            show_path=False,
        )
    else:
        console_handler = logging.StreamHandler(sys.stdout)

    console_handler.setLevel(level.upper())
    console_formatter = logging.Formatter("%(message)s")
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    # File handler (if specified)
    if log_file:
        log_file.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel("DEBUG")  # Always debug in file
        file_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "missionforge") -> logging.Logger:
    """Get logger instance.

    Args:
        name: Logger name.

    Returns:
        Logger instance.
    """
    return logging.getLogger(name)


# Made with Bob
