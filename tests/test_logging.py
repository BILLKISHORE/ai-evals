import logging
from ai_blackteam.logging_config import setup_logging, get_logger


def test_setup_logging_returns_logger():
    logger = setup_logging(level=logging.DEBUG)
    assert logger.name == "ai_blackteam"


def test_get_logger_returns_child():
    logger = get_logger("engine")
    assert logger.name == "ai_blackteam.engine"


def test_logging_does_not_duplicate_handlers():
    setup_logging()
    setup_logging()
    logger = logging.getLogger("ai_blackteam")
    # Should have at most 1 console handler (not duplicated)
    console_handlers = [h for h in logger.handlers if isinstance(h, logging.StreamHandler)]
    assert len(console_handlers) <= 2  # console + possibly file
