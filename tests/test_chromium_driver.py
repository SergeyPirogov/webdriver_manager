import os

import pytest
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType


def test_chromium_manager_with_specific_version():
    bin_path = ChromeDriverManager("2.26", chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(bin_path)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")

    path = ChromeDriverManager(version="2.26", path=custom_path, chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(path)
    assert custom_path in path


@pytest.mark.parametrize('path', [".", None])
def test_chromium_manager_with_latest_version(path):
    bin_path = ChromeDriverManager(path=path, chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(bin_path)


def test_chromium_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2", chrome_type=ChromeType.CHROMIUM).install()
    assert "There is no such driver by url" in ex.value.args[0]


def test_chromium_manager_with_selenium():
    driver_path = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    driver = webdriver.Chrome(driver_path)
    driver.get("http://automation-remarks.com")
    driver.close()


@pytest.mark.parametrize('path', [".", None])
def test_chromium_manager_cached_driver_with_selenium(path):
    ChromeDriverManager(path=path, chrome_type=ChromeType.CHROMIUM).install()
    webdriver.Chrome(ChromeDriverManager(path=path, chrome_type=ChromeType.CHROMIUM).install())


@pytest.mark.parametrize('path', [".", None])
def test_chromium_manager_with_win64_os(path):
    ChromeDriverManager(os_type="win64", path=path, chrome_type=ChromeType.CHROMIUM).install()


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chromium_for_win(os_type):
    path = ChromeDriverManager(os_type=os_type, chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(path)
