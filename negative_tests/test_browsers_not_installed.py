import os

import pytest
from selenium import webdriver
from selenium.common.exceptions import WebDriverException

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager, IEDriverManager
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import OSType, os_name, ChromeType


def test_brave_not_installed():
    binary_location = {
        OSType.LINUX: "/usr/bin/brave-browser",
        OSType.MAC: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        OSType.WIN: f"{os.getenv('LOCALAPPDATA')}\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    }[os_name()]

    option = webdriver.ChromeOptions()
    option.binary_location = binary_location
    driver_path = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
    with pytest.raises(WebDriverException):
        webdriver.Chrome(driver_path, options=option)


def test_chrome_not_installed():
    driver_path = ChromeDriverManager().install()
    with pytest.raises(WebDriverException):
        webdriver.Chrome(driver_path)


def test_firefox_not_installed():
    driver_path = GeckoDriverManager().install()
    with pytest.raises(WebDriverException):
        webdriver.Firefox(executable_path=driver_path)


def test_msedge_not_installed():
    driver_path = EdgeChromiumDriverManager().install()
    with pytest.raises(WebDriverException):
        webdriver.Edge(driver_path)
