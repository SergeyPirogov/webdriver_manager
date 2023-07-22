import json
import os

import pytest
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.constants import ROOT_FOLDER_NAME
from selenium.webdriver.chrome.service import Service as ChromeService

os.environ.setdefault("WDM_LOCAL", "true")


def test_chrome_manager_with_cache(delete_drivers_dir):
    ChromeDriverManager().install()
    driver_binary = ChromeDriverManager().install()
    assert os.path.exists(driver_binary)


def test_chrome_manager_with_specific_version(delete_drivers_dir):
    driver_binary = ChromeDriverManager("87.0.4280.88").install()
    assert os.path.exists(driver_binary)


def test_106_0_5249_61_chrome_version(delete_drivers_dir):
    driver_binary = ChromeDriverManager("106.0.5249.61").install()
    assert os.path.exists(driver_binary)


def test_chrome_manager_with_project_root_local_folder(delete_drivers_dir):
    os.environ['WDM_LOCAL'] = "1"
    driver_binary = ChromeDriverManager("87.0.4280.88").install()
    os.environ['WDM_LOCAL'] = "0"
    assert os.path.exists(driver_binary)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")
    path = ChromeDriverManager(version="87.0.4280.88", path=custom_path).install()
    assert os.path.exists(path)
    assert custom_path in path


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert "There is no such driver by url" in ex.value.args[0]


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(service=ChromeService(driver_path))
    driver.get("http://automation-remarks.com")
    driver.close()


def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(os.path.dirname(
        os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = ChromeDriverManager(path=custom_path).install()
    os.environ['WDM_SSL_VERIFY'] = '1'
    assert os.path.exists(driver_path)


def test_chrome_manager_cached_driver_with_selenium():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom-cache")
    manager = ChromeDriverManager(path=custom_path)
    driver = webdriver.Chrome(manager.install())
    driver.get("http://automation-remarks.com")

    metadata_file = os.path.join(custom_path, ROOT_FOLDER_NAME, 'drivers.json')

    with open(metadata_file) as json_file:
        data = json.load(json_file)

    for k in data.keys():
        data[k]['timestamp'] = "08/06/2019"

    with open(metadata_file, 'w') as outfile:
        json.dump(data, outfile)

    ChromeDriverManager(path=custom_path).install()


@pytest.mark.parametrize('os_type', ['win32', 'win64', 'mac64', 'mac64_m1'])
def test_can_get_chrome_for_os(os_type):
    path = ChromeDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
