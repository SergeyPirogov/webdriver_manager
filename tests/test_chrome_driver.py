import json
import os

import pytest
from selenium import webdriver

from webdriver_manager.chrome import ChromeDriverManager


def test_chrome_manager_with_specific_version():
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)


def test_driver_can_be_saved_to_custom_path():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")
    path = ChromeDriverManager(version="2.26", path=custom_path).install()
    assert os.path.exists(path)
    assert custom_path in path


def test_chrome_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        ChromeDriverManager("0.2").install()
    assert "There is no such driver by url" in ex.value.args[0]


def test_chrome_manager_with_selenium():
    driver_path = ChromeDriverManager().install()
    driver = webdriver.Chrome(driver_path)
    driver.get("http://automation-remarks.com")
    driver.close()


def test_chrome_manager_cached_driver_with_selenium():
    custom_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "custom")
    manager = ChromeDriverManager(path=custom_path)
    driver = webdriver.Chrome(manager.install())
    driver.get("http://automation-remarks.com")

    metadata_file = os.path.join(custom_path, 'drivers.json')

    with open(metadata_file) as json_file:
        data = json.load(json_file)

    for k in data.keys():
        data[k]['timestamp'] = "08/06/2019"

    with open(metadata_file, 'w') as outfile:
        json.dump(data, outfile)

    ChromeDriverManager(path=custom_path).install()


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_chrome_for_win(os_type):
    path = ChromeDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
