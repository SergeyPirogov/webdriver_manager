import os

import pytest
from selenium import webdriver

from webdriver_manager.firefox import GeckoDriverManager


def test_gecko_manager_with_selenium():
    driver_path = GeckoDriverManager().install()
    ff = webdriver.Firefox(executable_path=driver_path)
    ff.get("http://automation-remarks.com")
    ff.quit()


def test_driver_with_ssl_verify_disabled_can_be_downloaded():
    try:
        os.environ['WDM_SSL_VERIFY'] = '0'
        custom_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "ssl_disabled",
        )
        driver_path = GeckoDriverManager(path=custom_path).install()

        assert os.path.exists(driver_path)

    finally:
        os.environ['WDM_SSL_VERIFY'] = ''


def test_gecko_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        driver_path = GeckoDriverManager("0.2").install()
        ff = webdriver.Firefox(executable_path=driver_path)
        ff.quit()
    assert "There is no such driver by url "\
        "https://api.github.com/repos/mozilla/geckodriver/releases/tags/0.2" \
        in ex.value.args[0]


def test_gecko_manager_with_correct_version_and_token():
    driver_path = GeckoDriverManager(version="v0.11.0").install()
    assert os.path.exists(driver_path)


def test_can_download_ff_x64():
    driver_path = GeckoDriverManager(os_type="win64").install()
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'linux32',
                                     'linux64',
                                     'mac64'])
def test_can_get_driver_from_cache(os_type):
    GeckoDriverManager(os_type=os_type).install()
    driver_path = GeckoDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
