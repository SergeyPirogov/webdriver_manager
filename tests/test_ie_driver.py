import os
import platform
from unittest import skipUnless

import pytest

from webdriver_manager.microsoft import IEDriverManager


@pytest.mark.parametrize("version", [
    "3.0",
    "3.150.0"
])
@skipUnless(platform.system() == 'Windows', 'Windows required.')
def test_ie_manager_with_different_versions(version):
    path = IEDriverManager(version).install()
    assert os.path.exists(path)


@skipUnless(platform.system() == 'Windows', 'Windows required.')
def test_driver_with_ssl_verify_disabled_can_be_downloaded(ssl_verify_enable):
    os.environ['WDM_SSL_VERIFY'] = '0'
    custom_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "ssl_disabled",
    )
    driver_path = IEDriverManager(path=custom_path).install()
    os.environ['WDM_SSL_VERIFY'] = '1'
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
@skipUnless(platform.system() == 'Windows', 'Windows required.')
def test_can_download_ie_driver_x64(os_type):
    path = IEDriverManager(os_type=os_type).install()
    assert os.path.exists(path)


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
@skipUnless(platform.system() == 'Windows', 'Windows required.')
def test_can_get_ie_driver_from_cache(os_type):
    IEDriverManager(os_type=os_type).install()
    driver_path = IEDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
