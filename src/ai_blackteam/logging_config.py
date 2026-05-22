import logging
import sys
from pathlib import Path


def setup_logging(level=logging.INFO, log_file=None):
    """Configure logging for ai_blackteam.

    Args:
        level: logging level (default INFO)
        log_file: optional file path for log output
    """
    logger = logging.getLogger("ai_blackteam")
    logger.setLevel(level)

    # Don't add handlers if already configured
    if logger.handlers:
        return logger

    formatter = logging.Formatter(
        "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler (stderr)
    console = logging.StreamHandler(sys.stderr)
    console.setLevel(level)
    console.setFormatter(formatter)
    logger.addHandler(console)

    # File handler (optional)
    if log_file:
        path = Path(log_file)
        path.parent.mkdir(parents=True, exist_ok=True)
        file_handler = logging.FileHandler(str(path))
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name):
    """Get a child logger under the ai_blackteam namespace."""
    return logging.getLogger(f"ai_blackteam.{name}")
