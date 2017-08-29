import os
import sys

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
    ie_driver = IEDriver(version, "win32")
    if use_cache:
        cache.download_driver(ie_driver)
    ie_driver_bin = cache.download_driver(ie_driver)
    assert ie_driver_bin.name == u'IEDriverServer'
    assert os.path.exists(ie_driver_bin.path)


@pytest.mark.skipif(sys.platform != 'win32',
                    reason="run only on windows")
@pytest.mark.parametrize('path', PATH)
@pytest.mark.parametrize('with_path', [True,
                                       False])
def test_ie_driver_manager_with_wrong_version(path, with_path):
    with pytest.raises(ValueError) as ex:
        if with_path:
            delete_old_install(path)
            IEDriverManager("0.2").install(path)
        else:
            delete_old_install()
            IEDriverManager("0.2").install()
    assert ex.value.args[0] == "There is no such driver IEDriverServer with version 0.2 " \
                               "by http://selenium-release.storage.googleapis.com/0.2/IEDriverServer_Win32_0.2.0.zip"


def test_can_get_latest_ie_driver_version():
    latest_version = IEDriver("latest", "win32").get_latest_release_version()
    assert latest_version


def test_can_get_latest_ie_driver_for_x64():
    delete_old_install()
    IEDriverManager(os_type="win64").install()
