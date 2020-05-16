import logging
import os


class Logger(object):

    def __init__(self):
        os_wdm_log_level = int(os.getenv('WDM_LOG_LEVEL', logging.INFO))

        logger = logging.getLogger('WDM')

        handler = logging.StreamHandler()
        formatter = logging.Formatter('[%(name)s] - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(os_wdm_log_level)
        self.logger = logger

    def log(self, text):
        self.logger.info(text)
