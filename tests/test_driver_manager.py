import os

from webdriver_manager.driver_manager import ChromeDriverManager


def test_chrome_manager_with_specific_version():
    path = ChromeDriverManager("2.26").install()
    assert os.path.exists(path)


def test_chrome_manager_with_latest_version():
    path = ChromeDriverManager().install()
    assert os.path.exists(path)
