import os

import pytest

from webdriver_manager.microsoft import IEDriverManager


@pytest.mark.parametrize("version", [
    "3.0",
    "3.150.0"
])
def test_ie_manager_with_different_versions(version):
    path = IEDriverManager(version).install()
    assert os.path.exists(path)


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
def test_can_download_ie_driver_x64(os_type):
    path = IEDriverManager(os_type=os_type).install()
    assert os.path.exists(path)


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_ie_driver_from_cache(os_type):
    IEDriverManager(os_type=os_type).install()
    driver_path = IEDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('version', ['', '3', '3.4.5.6'])
def test__get_divided_version_raises_exception(version):
    iedriver = IEDriverManager().driver

    with pytest.raises(ValueError) as exception:
        iedriver._IEDriver__get_divided_version(version=version)

    expected_msg = (
        "Version must consist of major, minor and/or patch, "
        "but given was: '{}'".format(version)
    )
    assert str(exception.value) == expected_msg
