import os

import pytest
from selenium import webdriver

from webdriver_manager.chrome import ChromiumDriverManager


def test_chromium_manager_with_specific_version():
    bin_path = ChromiumDriverManager("2.27").install()
    assert os.path.exists(bin_path)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")

    path = ChromiumDriverManager(version="2.27", path=custom_path).install()
    assert os.path.exists(path)
    assert custom_path in path


@pytest.mark.parametrize('path', [".", None])
def test_chromium_manager_with_latest_version(path):
    bin_path = ChromiumDriverManager(path=path).install()
    assert os.path.exists(bin_path)


def test_chromium_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromiumDriverManager("0.2").install()
    assert "There is no such driver by url" in ex.value.args[0]


def test_chromium_manager_with_selenium():
    driver_path = ChromiumDriverManager().install()
    driver = webdriver.Chrome(driver_path)
    driver.get("http://automation-remarks.com")
    driver.close()


@pytest.mark.parametrize('path', [".", None])
def test_chromium_manager_cached_driver_with_selenium(path):
    ChromiumDriverManager(path=path).install()
    webdriver.Chrome(ChromiumDriverManager(path=path).install())


@pytest.mark.parametrize('path', [".", None])
def test_chromium_manager_with_win64_os(path):
    ChromiumDriverManager(os_type="win64", path=path).install()


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chromium_for_win(os_type):
    path = ChromiumDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
