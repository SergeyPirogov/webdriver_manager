import os

import pytest

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.os_manager import ChromeType, OperationSystemManager


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request:urllib3.exceptions.InsecureRequestWarning")
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = ChromeDriverManager(
        driver_version="115.0.5763.0",
        cache_manager=DriverCacheManager(custom_path),
        chrome_type=ChromeType.CHROMIUM,
    ).install()

    assert os.path.exists(driver_path)


def test_chromium_manager_with_specific_version():
    bin_path = ChromeDriverManager("115.0.5763.0", chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(bin_path)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")

    path = ChromeDriverManager(driver_version="115.0.5763.0", cache_manager=DriverCacheManager(custom_path),
                               chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(path)
    assert custom_path in path


def test_chromium_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2", chrome_type=ChromeType.CHROMIUM).install()
    assert "There is no such driver by url" in ex.value.args[0]


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chromium_for_win(os_type):
    path = ChromeDriverManager(driver_version="115.0.5763.0",
                               os_system_manager=OperationSystemManager(os_type=os_type),
                               chrome_type=ChromeType.CHROMIUM).install()
    assert os.path.exists(path)
