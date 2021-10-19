import os

import pytest

from webdriver_manager.microsoft import IEDriverManager


@pytest.mark.parametrize("version", [
    "2.53.1",
    "3.0",
    "3.13.0",
    "3.141.59",
    "3.150.0",
    # "3.150.1",
    # "3.150.2",
    "latest",
])
def test_ie_manager_with_different_versions(version):
    path = IEDriverManager(version).install()
    assert os.path.exists(path)


# def test_ie_manager_with_selenium():
#     driver_path = IEDriverManager().install()
#     if os.name == 'nt':
#         driver = webdriver.Ie(executable_path=driver_path)
#         driver.get("http://automation-remarks.com")
#         driver.quit()
#     else:
#         assert os.path.exists(driver_path)


def test_driver_with_ssl_verify_disabled_can_be_downloaded():
    try:
        os.environ['WDM_SSL_VERIFY'] = '0'
        custom_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "ssl_disabled",
        )
        driver_path = IEDriverManager(path=custom_path).install()

        assert os.path.exists(driver_path)

    finally:
        os.environ['WDM_SSL_VERIFY'] = ''


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_download_ie_driver_x64(os_type):
    path = IEDriverManager(os_type=os_type).install()
    assert os.path.exists(path)


@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_ie_driver_from_cache(os_type):
    IEDriverManager(os_type=os_type).install()
    driver_path = IEDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
