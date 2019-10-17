import os
import shutil

import pytest
from selenium import webdriver
from selenium.webdriver.chrome import service

from tests.test_cache import cache, delete_cache
from webdriver_manager.driver import OperaDriver
from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import os_type as get_os_type

PATH = '.'


def delete_old_install(path=None, os_type=None):
    if path is not None:
        path = os.path.abspath(path)
    if os_type is not None:
        os_type = get_os_type()
        try:
            os.remove(os.path.join(path, 'operadriver_{}.zip'.format(os_type)))
            shutil.rmtree(os.path.join(path, 'operadriver_{}'.format(os_type)))
        except OSError:
            pass
        except Exception:
            pass


def test_opera_driver_manager_with_correct_version():
    driver_path = OperaDriverManager("v.2.45").install()
    assert os.path.exists(driver_path)


def test_operadriver_manager_with_selenium():
    driver_path = OperaDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_argument('allow-elevated-browser')

    if get_os_type() == "win64":
        options.binary_location = ("C:\\Users\\{0}\\AppData\\Local\\Programs"
                                   "\\Opera\\{1}\\opera.exe"
                                   .format(os.getlogin(), "64.0.3417.54"))
    elif get_os_type() == "linux64" or "linux32" or "mac":
        options.binary_location = "/usr/bin/opera"

    ff = webdriver.Opera(executable_path=driver_path, options=options)
    ff.get("http://automation-remarks.com")
    ff.quit()


def test_opera_driver_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install(PATH)
        driver_path = OperaDriverManager("0.2").install()
        ff = webdriver.Opera(executable_path=driver_path)
        ff.quit()
        print(ex.value.args[0])
    assert ex.value.args[0] == "There is no such driver operadriver with "\
                               "version 0.2"


@pytest.mark.parametrize('path', [PATH])
def test_opera_driver_manager_with_correct_version_and_token(path):
    driver_path = OperaDriverManager("v.2.45").install(path)
    assert os.path.exists(driver_path)


def test_opera_driver_driver_with_wrong_token():
    old_token = os.getenv("GH_TOKEN", "default")
    os.environ["GH_TOKEN"] = "aaa"
    with pytest.raises(ValueError) as ex:
        driver = OperaDriver(version="latest",
                             os_type="linux32")
        cache.download_driver(driver)
    assert ex.value.args[0]['message'] == "Bad credentials"
    os.environ["GH_TOKEN"] = old_token


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'linux64',
                                     'mac64'])
def test_can_get_driver_from_cache(os_type):
    delete_cache()
    OperaDriverManager(os_type=os_type).install()
    driver_path = OperaDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
