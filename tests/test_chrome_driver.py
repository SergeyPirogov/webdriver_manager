import os

import pytest
from selenium import webdriver

from webdriver_manager import utils
from webdriver_manager.chrome import ChromeDriverManager

PATH = '.'


def test_chrome_manager_with_specific_version():
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)


@pytest.mark.parametrize('path', [PATH, None])
def test_chrome_manager_with_latest_version(path):
    bin = ChromeDriverManager().install(path)
    assert os.path.exists(bin)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert ex.value.args[
               0] == "There is no such driver by url http://chromedriver.storage.googleapis.com/0.2/chromedriver_{0}.zip".format(
        utils.os_type())


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install()
    webdriver.Chrome(driver_path)


@pytest.mark.parametrize('path', [PATH, None])
def test_chrome_manager_cached_driver_with_selenium(path):
    ChromeDriverManager().install(path)
    webdriver.Chrome(ChromeDriverManager().install(path))


@pytest.mark.parametrize('path', [PATH, None])
def test_chrome_manager_with_win64_os(path):
    ChromeDriverManager(os_type="win64").install(path)


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chrome_for_win(os_type):
    path = ChromeDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
