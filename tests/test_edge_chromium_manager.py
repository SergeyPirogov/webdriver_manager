import os

import pytest
from selenium import webdriver
from selenium.webdriver import DesiredCapabilities

from tests.test_cache import delete_cache
from webdriver_manager.drivers.driver import ChromeDriver
from webdriver_manager.drivers.microsoft import EdgeChromiumDriverManager

PATH = '.'


def delete_old_install(path=None):
    if path is None:
        delete_cache()
    else:
        path = os.path.abspath(path)
        for f in os.listdir(path):
            if f.startswith("phantomjs-"):
                try:
                    os.remove(os.path.join(path, f))
                except Exception as e:
                    pass


def test_edge_chromium_manager_with_specific_version():
    bin = EdgeChromiumDriverManager("80.0.319.0", os_type="win32").install()
    assert os.path.exists(bin)


@pytest.mark.parametrize('path', [PATH, None])
def test_edge_chromium_manager_with_latest_version(path):
    bin = EdgeChromiumDriverManager().install(path)
    assert os.path.exists(bin)


def test_edge_chromium_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install()
        EdgeChromiumDriverManager("0.2", os_type="win32").install()
    assert ex.value.args[0] == "There is no such driver EdgeDriver with version 0.2 " \
                               "by https://msedgedriver.azureedge.net/0.2/edgedriver_win32.zip"


def test_edge_chromium_manager_with_selenium():
    delete_old_install()
    driver_path = EdgeChromiumDriverManager().install()
    webdriver.Chrome(driver_path)


@pytest.mark.parametrize('path', [PATH, None])
def test_edge_chromium_manager_cached_driver_with_selenium(path):
    EdgeChromiumDriverManager().install(path)
    webdriver.Chrome(EdgeChromiumDriverManager().install(path))


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_edge_chromium_for_windows(os_type):
    delete_cache()
    path = EdgeChromiumDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
