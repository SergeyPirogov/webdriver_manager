import logging

from webdriver_manager.core.config import wdm_log_level

__logger = logging.getLogger("WDM")

__logger.setLevel(wdm_log_level())

def log(text):
    """Emitting the log message."""
    __logger.info(text)
