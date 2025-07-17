import glob
import os
import shutil

import browsers
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.service import Service

from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.core.os_manager import OperationSystemManager
from webdriver_manager.opera import OperaDriverManager


def test_opera_driver_manager_with_correct_version(delete_drivers_dir):
    driver_path = OperaDriverManager("v.2.45").install()
    assert os.path.exists(driver_path)


@pytest.mark.filterwarnings("ignore:Unverified HTTPS request:urllib3.exceptions.InsecureRequestWarning")
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = OperaDriverManager(cache_manager=DriverCacheManager(custom_path)).install()
    os.environ['WDM_SSL_VERIFY'] = '1'
    assert os.path.exists(driver_path)


def test_operadriver_manager_with_selenium():
    driver_path = OperaDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_experimental_option('w3c', True)
    binary_location = browsers.get("opera")
    if not binary_location:
        pytest.skip("Opera not found")
    options.binary_location = binary_location["path"]
    web_service = Service(driver_path)
    web_service.start()

    opera_driver = webdriver.Remote(web_service.service_url, options=options)
    opera_driver.get("http://automation-remarks.com")
    opera_driver.quit()


def test_opera_driver_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        OperaDriverManager("0.2").install()

    assert "There is no such driver by url " \
           "https://api.github.com/repos/operasoftware/operachromiumdriver/" \
           "releases/tags/0.2" in ex.value.args[0]


@pytest.mark.parametrize('path', ['.', None])
def test_opera_driver_manager_with_correct_version_and_token(path):
    driver_path = OperaDriverManager(version="v.2.45", cache_manager=DriverCacheManager(path)).install()
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'linux64',
                                     'mac64'])
def test_can_get_driver_from_cache(os_type, delete_drivers_dir):
    OperaDriverManager(os_system_manager=OperationSystemManager(os_type)).install()
    driver_path = OperaDriverManager(os_system_manager=OperationSystemManager(os_type)).install()
    assert os.path.exists(driver_path)
