import logging
import os

from webdriver_manager.utils import console


class TestWdmLogLevelEnvironmentVariable:
    """Test silent logs and logging levels passing to webdriver_manager through
    WDM_LOG_LEVEL environment variable

    CRITICAL = 50
    ERROR = 40
    WARNING = 30
    INFO = 20
    DEBUG = 10
    NOTSET = 0
    """
    see_message = 'You should SEE this message'

    def test_default_wdmlog_returns_info(self):
        console(self.see_message)

    def test_notset_level_returns_nothing(self):
        message = 'You should NOT see this message'
        os.environ['WDM_LOG_LEVEL'] = str(logging.NOTSET)
        console(message)

    def test_debug_level_returns_debug(self):
        os.environ['WDM_LOG_LEVEL'] = str(logging.DEBUG)
        console(self.see_message)

    def test_info_level_returns_info(self):
        os.environ['WDM_LOG_LEVEL'] = str(logging.INFO)
        console(self.see_message)

    def test_warning_level_returns_warning(self):
        os.environ['WDM_LOG_LEVEL'] = str(logging.WARNING)
        console(self.see_message)

    def test_error_level_returns_error(self):
        os.environ['WDM_LOG_LEVEL'] = str(logging.ERROR)
        console(self.see_message)

    def test_critical_level_returns_critical(self):
        os.environ['WDM_LOG_LEVEL'] = str(logging.CRITICAL)
        console(self.see_message)
