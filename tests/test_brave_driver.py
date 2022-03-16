import os

import pytest
from selenium import webdriver
import logging

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.utils import ChromeType, os_name, OSType
from webdriver_manager.logger import logger


def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = ChromeDriverManager(
        version="83.0.4103.39",
        path=custom_path,
        chrome_type=ChromeType.BRAVE,
    ).install()

    assert os.path.exists(driver_path)


def test_brave_manager_with_specific_version():
    bin_path = ChromeDriverManager("2.27", chrome_type=ChromeType.BRAVE).install()
    assert os.path.exists(bin_path)


def test_brave_manager_with_selenium():
    binary_location = {
        OSType.LINUX: "/usr/bin/brave-browser",
        OSType.MAC: "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
        OSType.WIN: f"{os.getenv('LOCALAPPDATA')}\\BraveSoftware\\Brave-Browser\\Application\\brave.exe",
    }[os_name()]
    logger.info(binary_location)
    option = webdriver.ChromeOptions()
    option.binary_location = binary_location
    driver_path = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
    driver = webdriver.Chrome(driver_path, options=option)

    driver.get("http://automation-remarks.com")
    driver.close()


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")

    path = ChromeDriverManager(version="2.27", path=custom_path,
                               chrome_type=ChromeType.BRAVE).install()
    assert os.path.exists(path)
    assert custom_path in path


def test_brave_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2", chrome_type=ChromeType.BRAVE).install()
    assert "There is no such driver by url" in ex.value.args[0]


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_brave_for_win(os_type):
    path = ChromeDriverManager(version="83.0.4103.39", os_type=os_type,
                               chrome_type=ChromeType.BRAVE).install()
    assert os.path.exists(path)
