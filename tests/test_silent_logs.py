import os

from webdriver_manager.chrome import ChromeDriverManager


def test_chrome_manager_with_logs_level_0_set_locally():
    os.environ['WDM_LOG_LEVEL'] = '0'
    bin = ChromeDriverManager("2.26", log_level=20).install()
    assert os.path.exists(bin)
