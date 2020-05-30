import os
import pytest
from selenium import webdriver
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.utils import os_name, os_type


# TODO: set 'if os_name() != 'linux':
# when edge > 82 is installed on mac os worker
def test_edge_manager_with_selenium():
    if os_name() == 'win':
        driver_path = EdgeChromiumDriverManager(os_type=os_type()).install()
        driver = webdriver.Edge(executable_path=driver_path)
        driver.get("http://automation-remarks.com")
        driver.quit()
    else:
        driver_path = EdgeChromiumDriverManager(os_type="win32").install()
        assert os.path.exists(driver_path)


def test_edge_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        driver_path = EdgeChromiumDriverManager("0.2",
                                                os_type='win64').install()
        driver = webdriver.Edge(executable_path=driver_path)
        driver.quit()
    assert "There is no such driver by url "\
        "https://msedgedriver.azureedge.net/0.2/edgedriver_win64.zip" in \
           ex.value.args[0]


# TODO: add "mac64" when https://msedgedriver.azureedge.net/LATEST_STABLE
# return edgedriver > 82
# see:
# https://msedgewebdriverstorage.z22.web.core.windows.net/?prefix=82.0.418.0/
@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_download_edge_driver(os_type):
    path = EdgeChromiumDriverManager(os_type=os_type).install()
    assert os.path.exists(path)


# TODO: add "mac64" when https://msedgedriver.azureedge.net/LATEST_STABLE
# return edgedriver > 82
# see:
# https://msedgewebdriverstorage.z22.web.core.windows.net/?prefix=82.0.418.0/
@pytest.mark.parametrize('os_type', ['win32', 'win64'])
def test_can_get_edge_driver_from_cache(os_type):
    EdgeChromiumDriverManager(os_type=os_type).install()
    driver_path = EdgeChromiumDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)


def test_edge_with_specific_version():
    bin_path = EdgeChromiumDriverManager("77.0.189.3",
                                         os_type='win64').install()
    assert os.path.exists(bin_path)
