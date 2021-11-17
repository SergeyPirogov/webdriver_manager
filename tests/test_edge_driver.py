import os

import pytest
from selenium import webdriver

from webdriver_manager.microsoft import EdgeChromiumDriverManager


def test_edge_manager_with_selenium():
    driver_path = EdgeChromiumDriverManager().install()

    driver = webdriver.Edge(executable_path=driver_path, capabilities={})

    driver.get("http://automation-remarks.com")
    driver.quit()


def test_driver_with_ssl_verify_disabled_can_be_downloaded():
    try:
        os.environ['WDM_SSL_VERIFY'] = '0'
        custom_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "ssl_disabled",
        )
        driver_path = EdgeChromiumDriverManager(path=custom_path).install()

        assert os.path.exists(driver_path)

    finally:
        os.environ['WDM_SSL_VERIFY'] = ''


def test_edge_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        driver_path = EdgeChromiumDriverManager(
            version="0.2",
            os_type='win64',
        ).install()
        driver = webdriver.Edge(executable_path=driver_path)
        driver.quit()

    assert (
               "There is no such driver by url "
               "https://msedgedriver.azureedge.net/0.2/edgedriver_win64.zip"
           ) in ex.value.args[0]


@pytest.mark.parametrize('os_type', ['win32', 'win64', 'mac64', 'linux64'])
@pytest.mark.parametrize('specific_version', ['86.0.600.0'])
def test_edge_with_specific_version(os_type, specific_version):
    bin_path = EdgeChromiumDriverManager(
        version=specific_version,
        os_type=os_type,
    ).install()
    assert os.path.exists(bin_path)


@pytest.mark.parametrize('os_type', ['win32', 'win64', 'mac64', 'linux64'])
@pytest.mark.parametrize('specific_version', ['87.0.637.0'])
def test_can_get_edge_driver_from_cache(os_type, specific_version):
    EdgeChromiumDriverManager(
        version=specific_version,
        os_type=os_type,
    ).install()
    driver_path = EdgeChromiumDriverManager(
        version=specific_version,
        os_type=os_type
    ).install()
    assert os.path.exists(driver_path)
