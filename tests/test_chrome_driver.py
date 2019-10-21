import os

import pytest
from selenium import webdriver

from webdriver_manager import utils
from webdriver_manager.chrome import ChromeDriverManager

PATH = '.'


def test_chrome_manager_with_specific_version():
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    os_type = "win32" if utils.os_type() == "win64" else utils.os_type()
    ex_value = ("There is no such driver by url "
                "http://chromedriver.storage.googleapis.com/0.2/"
                "chromedriver_{0}.zip".format(os_type))
    assert ex.value.args[0] == ex_value


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver_path)
    driver.get("http://automation-remarks.com")
    driver.close()


def test_chrome_manager_cached_driver_with_selenium():
    ChromeDriverManager().install()
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("http://automation-remarks.com")
    driver.close()


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chrome_for_win(os_type):
    path = ChromeDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
