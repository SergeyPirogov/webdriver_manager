import logging

from webdriver_manager.core.config import wdm_log_level

__logger = logging.getLogger("WDM")

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(name)s] - %(message)s")
handler.setFormatter(formatter)
__logger.addHandler(handler)


def log(text):
    """Emitting the log message."""
    __logger.log(wdm_log_level, text)
