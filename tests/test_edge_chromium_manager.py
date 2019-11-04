import glob
import os
import shutil

import pytest
import selenium as se
from selenium import webdriver
from webdriver_manager.drivers.microsoft import EdgeChromiumDriverManager
from webdriver_manager.utils import os_type as get_os_type

PATH = '.'


def delete_old_install(path=None):
    if path is not None:
        path = os.path.abspath(path)
    os_type = get_os_type()
    try:
        os.remove(os.path.join(path, 'edgedriver_{}.zip'.format(os_type)))
        shutil.rmtree(os.path.join(path, 'edgedriver_{}'.format(os_type)))
    except OSError:
        pass
    except Exception:
        pass


def test_edge_chromium_manager_with_correct_version():
    driver_path = EdgeChromiumDriverManager("80.0.320.0").install()
    assert os.path.exists(driver_path)


def test_edge_chromium_manager_with_selenium():
    driver_path = EdgeChromiumDriverManager().install()
    options = webdriver.EdgeOptions(is_legacy=False)
    if get_os_type() == "win64" or "win32":
        path = "C:\\Users\\{0}\\AppData\\Local\\Microsoft\\Edge SxS\\Application\\msedge.exe".format(os.getlogin())

        if os.path.isfile(path) and path == "msedge.exe":
            options.binary_location = path
    elif (get_os_type() or "mac64") and not os.path.exists('/usr/bin/msedge'):
        path = "/usr/bin/msedge"
    if se.__version__.startswith('4'):
        edge = webdriver.ChromiumEdge(executable_path=driver_path, options=options, port=9516)
        edge.get("http://automation-remarks.com")
        edge.quit()
    else:
        assert False


def test_edge_chromium_manager_with_wrong_version():
    with pytest.raises(ValueError) as ex:
        delete_old_install()
        driver_path = EdgeChromiumDriverManager("0.2").install()
    assert "There is no such driver by url https://msedgedriver.azureedge.net/0.2/edgedriver_win64.zip" in \
           ex.value.args[0]


def test_can_download_ff_x64():
    driver_path = EdgeChromiumDriverManager(os_type="win64").install()
    assert os.path.exists(driver_path)


@pytest.mark.parametrize('os_type', ['win32',
                                     'win64',
                                     'mac64'])
def test_can_get_driver_from_cache(os_type):
    EdgeChromiumDriverManager(os_type=os_type).install()
    driver_path = EdgeChromiumDriverManager(os_type=os_type).install()
    assert os.path.exists(driver_path)
