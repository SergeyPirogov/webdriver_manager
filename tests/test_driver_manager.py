import os
from selenium import webdriver
import pytest

from webdriver_manager.driver_manager import ChromeDriverManager


def test_chrome_manager_with_specific_version():
    path = ChromeDriverManager("2.27").install()
    assert os.path.exists(path)


def test_chrome_manager_with_latest_version():
    path = ChromeDriverManager().install()
    assert os.path.exists(path)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert ex.value.message == "No such driver found by url " \
                               "http://chromedriver.storage.googleapis.com/0.2/chromedriver_mac64.zip." \
                               " Wrong url or driver version"


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install()
    webdriver.Chrome(driver_path)
