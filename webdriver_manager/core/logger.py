import logging

from webdriver_manager.core.config import wdm_log_level

__logger = logging.getLogger("WDM")
__logger.addHandler(logging.NullHandler())


def log(text):
    """Emitting the log message."""
    __logger.log(wdm_log_level(), text)
