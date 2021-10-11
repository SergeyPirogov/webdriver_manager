import logging
import os

logger = logging.getLogger('WDM')

def _init_logger(level=logging.INFO):
    """Initialize the logger."""
    log_level = os.getenv('WDM_LOG_LEVEL')
    if log_level:
        level = int(log_level)
    logger.setLevel(level)
    
_init_logger()
