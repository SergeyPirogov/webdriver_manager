import logging
import os

loggers = {}

def _init_logger(level=logging.INFO, name="WDM", first_line=False, formatter='[%(name)s] - %(message)s'):
    """Initialize the logger."""
    log_level = os.getenv('WDM_LOG_LEVEL')
    if log_level:
        level = int(log_level)
    if not loggers.get(name):
        _logger = logging.getLogger(name)

        handler = logging.StreamHandler()
        formatter = logging.Formatter(formatter)
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(level)
        loggers[name] = _logger

def log(text, level=logging.INFO, name="WDM", first_line=False, formatter='[%(name)s] - %(message)s'):
    """Emitting the log message."""
    _init_logger(level, name, first_line, formatter)
    loggers.get(name).info(text)
    
_init_logger()
