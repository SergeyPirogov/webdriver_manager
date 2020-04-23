import os

import pytest

from webdriver_manager.microsoft import EdgeChromiumDriverManager

PATH = '.'


@pytest.mark.parametrize("version", ["2.53.1",
                                     "3.0",
                                     "latest"])
def test_ie_manager_with_selenium(version):
    driver_path = EdgeChromiumDriverManager(version, os_type="win32").install()
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_download_edge_driver_x64(os_type):
    path = EdgeChromiumDriverManager(os_type=os_type).install()
    assert os.path.exists(path)
