import logging

loggers = {}
__logger = logging.getLogger("WDM")

__logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter("[%(name)s] - %(message)s")
handler.setFormatter(formatter)
__logger.addHandler(handler)


def log(text):
    """Emitting the log message."""
    __logger.info(text)
