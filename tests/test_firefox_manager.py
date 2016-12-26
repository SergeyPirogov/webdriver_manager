import os

import pytest
from selenium import webdriver

from webdriver_manager.firefox import GeckoDriverManager

def test_gecko_manager_with_correct_version():
    driver_path = GeckoDriverManager("v0.11.0").install()
    assert os.path.exists(driver_path)


def test_gecko_manager_with_selenium():
    driver_path = GeckoDriverManager().install()
    ff = webdriver.Firefox(executable_path=
                           driver_path)
    ff.get("http://automation-remarks.com")
    ff.quit()


def test_gecko_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        driver_path = GeckoDriverManager("0.2").install()
        ff = webdriver.Firefox(executable_path=
                               driver_path)
        ff.quit()
    assert ex.value.message == "There is no such driver geckodriver with version 0.2"
