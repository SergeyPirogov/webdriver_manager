import os
import sys
from os.path import expanduser

import pytest
from selenium import webdriver

from tests.test_cache import cache, delete_cache
from webdriver_manager.driver import IEDriver
from webdriver_manager.microsoft import IEDriverManager

PATH = '.'


def delete_old_install(path=None):
    if path is None:
        delete_cache()
    else:
        path = os.path.abspath(path)
        try:
            os.remove(os.path.join(path, 'IEDriverServer.exe'))
            os.remove(os.path.join(path, 'IEDriverServer.zip'))
        except:
            pass


@pytest.mark.parametrize("version", ["2.53.1",
                                     "3.0",
                                     "latest",
                                     None])
@pytest.mark.parametrize("use_cache", [True,
                                       False])
@pytest.mark.skipif(sys.platform != 'win32',
                    reason="run only on windows")
def test_ie_manager_with_selenium(version, use_cache):
    delete_old_install()
    if use_cache:
        IEDriverManager(version).install()
    driver_path = IEDriverManager(version).install()
    dr = webdriver.Ie(driver_path)
    dr.quit()


@pytest.mark.parametrize("version", ["2.53.1",
                                     "3.0",
                                     "3.0.0",
                                     "latest",
                                     None])
@pytest.mark.parametrize("use_cache", [True,
                                       False])
def test_ie_driver_binary(version, use_cache):
    delete_old_install()
    if use_cache:
        IEDriverManager(version).install()
    ie_driver_bin = IEDriverManager(version, "win32").install()
    assert ie_driver_bin == os.path.join(expanduser("~"), ".wdm", "drivers", "IEDriverServer", version, "Win32",
                                         u'IEDriverServer.exe')
    assert os.path.exists(ie_driver_bin)


@pytest.mark.skipif(sys.platform != 'win32',
                    reason="run only on windows")
@pytest.mark.parametrize('path', [PATH, None])
def test_ie_driver_manager_with_wrong_version(path):
    with pytest.raises(ValueError) as ex:
        delete_old_install(path)
        IEDriverManager("0.2").install(path)
    assert "There is no such driver IEDriverServer with version 0.2" in ex.value.args[0]


def test_can_get_latest_ie_driver_version():
    latest_version = IEDriver("latest", "win32").get_latest_release_version()
    assert latest_version


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_download_ie_driver_x64(os_type):
    delete_old_install()
    path = IEDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
