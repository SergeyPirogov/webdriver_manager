"""tests.test_custom_logger.py"""

import logging
from pathlib import Path

import pytest

from webdriver_manager.core.logger import log, set_logger, __logger


# Log file path
log_file = Path(__file__).resolve().parents[1].joinpath(".wdm/logs/WDM_DEBUG.log")
# Create .wdm/logs directory
log_file.parent.mkdir(parents=True, exist_ok=True)

# Cache the old logger to restore it later
__old_logger = __logger


@pytest.fixture
def create_logger():
    """Create a logger."""

    # Create a Custom Debug Logger
    logger = logging.getLogger("WDM-DEBUG")
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.FileHandler(log_file))

    return logger


def test_custom_logger(create_logger):
    """Test the custom logger."""

    # Set the custom logger
    set_logger(create_logger)

    # send a log message
    log("This is a test log message")

    # Check if the log file exists
    assert log_file.exists()

    # Check if the log file contains the log message
    assert "This is a test log message" in log_file.read_text()

    # Delete the contents of the log file
    open(log_file, "w").close()

    # Restore the old logger
    set_logger(__old_logger)
