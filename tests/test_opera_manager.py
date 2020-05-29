import glob
import os

import pytest
from selenium import webdriver

from webdriver_manager.opera import OperaDriverManager
from webdriver_manager.utils import os_type as get_os_type


def test_opera_driver_manager_with_correct_version():
    driver_path = OperaDriverManager("v.2.45").install()
    assert os.path.exists(driver_path)


def test_operadriver_manager_with_selenium():
    driver_path = OperaDriverManager().install()
    options = webdriver.ChromeOptions()
    options.add_argument('allow-elevated-browser')

    if get_os_type() in ["win64", "win32"]:
        paths = [f for f in glob.glob(f"C:/Users/{os.getlogin()}/AppData/" \
                                      "Local/Programs/Opera/**",
                                      recursive=True)]
        for path in paths:
            if os.path.isfile(path) and path.endswith("opera.exe"):
                options.binary_location = path
    elif ((get_os_type() in ["linux64", "linux32"]) and not
          os.path.exists('/usr/bin/opera')):
        options.binary_location = "/usr/bin/opera"
    elif get_os_type() in "mac64":
        options.binary_location = "/Applications/Opera.app/Contents/MacOS/Opera"

    ff = webdriver.Opera(executable_path=driver_path, options=options)
    ff.get("http://automation-remarks.com")
    ff.quit()


def test_opera_driver_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        driver_path = OperaDriverManager("0.2").install()
        ff = webdriver.Opera(executable_path=driver_path)
        ff.quit()
    assert "There is no such driver by url " \
           "https://api.github.com/repos/operasoftware/operachromiumdriver/" \
           "releases/tags/0.2" in ex.value.args[0]


@pytest.mark.parametrize('path', ['.', None])
def test_opera_driver_manager_with_correct_version_and_token(path):
    driver_path = OperaDriverManager(version="v.2.45", path=path).install()
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'linux64',
                                     'mac64'])
def test_can_get_driver_from_cache(os_type):
    OperaDriverManager(os_type=os_type).install()
    driver_path = OperaDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
