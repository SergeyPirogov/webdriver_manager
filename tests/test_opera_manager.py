import os

import pytest
from selenium import webdriver

from tests.test_cache import cache, delete_cache
from webdriver_manager.driver import OperaDriver
from webdriver_manager.opera import OperaDriverManager

PATH = '.'


def delete_old_install(path=None):
    if path is not None:
        path = os.path.abspath(path)
        try:
            os.remove(os.path.join(os.path.dirname(path)))  # maybe change this
        except OSError as e:
            pass
        except Exception as e:
            pass


def test_operachromium_manager_with_correct_version():
    driver_path = OperaDriverManager("v.2.45").install()
    assert os.path.exists(driver_path)


def test_operachromium_manager_with_selenium():
    pass
    # driver_path = OperaDriverManager().install()
    # chrome_options = webdriver.ChromeOptions()
    # #getting error without this line
    # chrome_options.binary_location = "C:\\Users\\USERNAME\\FOLDERLOCATION\\Opera\\VERSION\\opera.exe"
    # ff = webdriver.Opera(executable_path=driver_path,
    #                      log_path=os.path.join(os.path.dirname(__file__), "log.log"),
    #                      options=chrome_options)
    # ff.get("http://automation-remarks.com")
    # ff.quit()


def test_operachromium_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install()
        driver_path = OperaDriverManager("0.2").install()
        ff = webdriver.Opera(executable_path=driver_path)
        ff.quit()
    assert ex.value.args[0] == "There is no such driver operachromiumdriver with version 0.2"


@pytest.mark.parametrize('path', [PATH, None])
def test_operachromium_manager_with_correct_version_and_token(path):
    driver_path = OperaDriverManager("v.2.45").install(path)
    assert os.path.exists(driver_path)


def test_operachromium_driver_with_wrong_token():
    old_token = os.getenv("GH_TOKEN", "default")
    os.environ["GH_TOKEN"] = "aaa"
    with pytest.raises(ValueError) as ex:
        driver = OperaDriver(version="latest",
                             os_type="linux32")
        cache.download_driver(driver)
    assert ex.value.args[0]['message'] == "Bad credentials"
    os.environ["GH_TOKEN"] = old_token


def test_can_download_ff_x64():
    delete_cache()
    driver_path = OperaDriverManager(os_type="win64").install()
    print(driver_path)


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'linux32',
                                     'linux64',
                                     'mac64'])
def test_can_get_driver_from_cache(os_type):
    delete_cache()
    OperaDriverManager(os_type=os_type).install()
    driver_path = OperaDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
