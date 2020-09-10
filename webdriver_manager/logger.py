import logging
import os

loggers = {}


def log(text, level=logging.INFO, name="WDM", first_line=False):
    log_level = os.getenv('WDM_LOG_LEVEL')
    print_first_line = os.getenv('WDM_PRINT_FIRST_LINE', default='true').lower() == 'true'
    if first_line and print_first_line and log_level != '0':
        print(" ")
    if log_level:
        level = int(log_level)
    if loggers.get(name):
        loggers.get(name).info(text)
    else:
        _logger = logging.getLogger(name)

        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(name)s] - %(message)s')
        handler.setFormatter(formatter)
        _logger.addHandler(handler)
        _logger.setLevel(level)
        loggers[name] = _logger
        _logger.info(text)
