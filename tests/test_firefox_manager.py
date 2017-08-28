import os

import pytest
from selenium import webdriver

from tests.test_cache import cache
from webdriver_manager.driver import GeckoDriver
from webdriver_manager.firefox import GeckoDriverManager

PATH = '.'

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_gecko_manager_with_correct_version(path, with_path):
    if path:
        driver_path = GeckoDriverManager("v0.11.0").install(path)
    else:
        driver_path = GeckoDriverManager("v0.11.0").install()
    assert os.path.exists(driver_path)

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_gecko_manager_with_selenium(path, with_path):
    if with_path:
        driver_path = GeckoDriverManager().install()
    else:
        driver_path = GeckoDriverManager().install()
    ff = webdriver.Firefox(executable_path=driver_path,
                           log_path=os.path.join(os.path.dirname(__file__), "log.log"))
    ff.get("http://automation-remarks.com")
    ff.quit()

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_gecko_manager_with_wrong_version(path, with_path):
    with pytest.raises(ValueError) as ex:
        if with_path:
            driver_path = GeckoDriverManager("0.2").install(path)
        else:
            driver_path = GeckoDriverManager("0.2").install()
        ff = webdriver.Firefox(executable_path=driver_path)
        ff.quit()
    assert ex.value.args[0] == "There is no such driver geckodriver with version 0.2"

@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_gecko_manager_with_correct_version_and_token(path, with_path):
    if with_path:
        driver_path = GeckoDriverManager("v0.11.0").install(path)
    else:
        driver_path = GeckoDriverManager("v0.11.0").install()
    assert os.path.exists(driver_path)


def test_gecko_driver_with_wrong_token():
    with pytest.raises(ValueError) as ex:
        driver = GeckoDriver(version="latest",
                             os_type="linux32")
        driver.config.set("gh_token", "adasda")
        cache.download_driver(driver)
    assert ex.value.args[0]['message'] == "Bad credentials"
