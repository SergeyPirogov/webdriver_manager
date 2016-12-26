import os

import pytest
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import OSUtils


def test_chrome_manager_with_specific_version():
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin.path)


def test_chrome_manager_with_latest_version():
    bin = ChromeDriverManager().install()
    assert os.path.exists(bin.path)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert ex.value.message == "There is no such driver chromedriver with version 0.2 " \
                               "by http://chromedriver.storage.googleapis.com/0.2/chromedriver_{0}.zip".format(
        OSUtils.os_type())


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install().path
    webdriver.Chrome(driver_path)
