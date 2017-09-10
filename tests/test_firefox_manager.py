import os

import pytest
from selenium import webdriver

from tests.test_cache import cache
from webdriver_manager.driver import GeckoDriver
from webdriver_manager.firefox import GeckoDriverManager

PATH = '.'


def delete_old_install(path=None):
    if not path is None:
        path = os.path.abspath(path)
        try:
            os.remove(os.path.join(path, 'geckodriver.exe'))
            os.remove(os.path.join(path, 'geckodriver.zip'))
        except:
            pass


def test_gecko_manager_with_correct_version():
    driver_path = GeckoDriverManager("v0.11.0").install()
    assert os.path.exists(driver_path)


def test_gecko_manager_with_selenium():
    driver_path = GeckoDriverManager().install()
    ff = webdriver.Firefox(executable_path=driver_path,
                           log_path=os.path.join(os.path.dirname(__file__), "log.log"))
    ff.get("http://automation-remarks.com")
    ff.quit()


def test_gecko_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install()
        driver_path = GeckoDriverManager("0.2").install()
        ff = webdriver.Firefox(executable_path=driver_path)
        ff.quit()
    assert ex.value.args[0] == "There is no such driver geckodriver with version 0.2"

@pytest.mark.parametrize('path', [PATH, None])
def test_gecko_manager_with_correct_version_and_token(path):
    driver_path = GeckoDriverManager("v0.11.0").install(path)
    assert os.path.exists(driver_path)


def test_gecko_driver_with_wrong_token():
    with pytest.raises(ValueError) as ex:
        driver = GeckoDriver(version="latest",
                             os_type="linux32")
        driver.config.set("gh_token", "adasda")
        cache.download_driver(driver)
    assert ex.value.args[0]['message'] == "Bad credentials"
