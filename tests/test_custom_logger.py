"""tests.test_custom_logger.py"""

import logging

import pytest

from webdriver_manager.core.logger import log, set_logger, __logger

# Cache the old logger to restore it later
__old_logger = __logger


@pytest.fixture
def create_logger():
    """Create a logger."""

    # Create a Custom Debug Logger
    logger = logging.getLogger("WDM-DEBUG")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())

    return logger


def test_custom_logger(capsys, create_logger):
    """Test the custom logger."""

    # Set the custom logger
    set_logger(create_logger)

    # send a log message
    log_msg = "This is a test log message from the custom logger"
    log(log_msg)

    # Check if the log message is in the output
    captured = capsys.readouterr()
    assert log_msg in captured.err
    capsys.close()

    # Restore the old logger
    set_logger(__old_logger)
