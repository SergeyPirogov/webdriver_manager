import os

import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.logger import log
from webdriver_manager.core.os_manager import ChromeType, OSType, OperationSystemManager


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request:urllib3.exceptions.InsecureRequestWarning")
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        '.wdm',
        "ssl_disabled",
    )
    driver_path = ChromeDriverManager(
        driver_version="115.0.5763.0",
        cache_manager=DriverCacheManager(custom_path),
        chrome_type=ChromeType.BRAVE,
    ).install()

    assert os.path.exists(driver_path)


def test_brave_manager_with_specific_version():
    bin_path = ChromeDriverManager("115.0.5763.0", chrome_type=ChromeType.BRAVE).install()
    assert os.path.exists(bin_path)


def test_brave_manager_with_selenium():
    # ths works on linux
    brave_path = shutil.which("brave")
    if not brave_path:
        pytest.skip("Brave browser not found in PATH")
    
    options = webdriver.ChromeOptions()
    options.binary_location = brave_path
    driver_path = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()

    service = Service(executable_path=driver_path)
    driver = webdriver.Chrome(service=service, options=options)

    driver.get("http://automation-remarks.com")
    driver.close()


def test_brave_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2", chrome_type=ChromeType.BRAVE).install()
    assert "There is no such driver by url" in ex.value.args[0]


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_brave_for_win(os_type):
    path = ChromeDriverManager(driver_version="115.0.5763.0",
                               os_system_manager=OperationSystemManager(os_type),
                               chrome_type=ChromeType.BRAVE).install()
    assert os.path.exists(path)
