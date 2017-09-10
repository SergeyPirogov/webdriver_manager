import os
import pytest
import sys

from tests.test_cache import cache
from tests.test_chrome_driver import delete_cache
from webdriver_manager.driver import EdgeDriver
from webdriver_manager.microsoft import EdgeDriverManager
from selenium import webdriver

PATH = '.'

def delete_old_install(path=None):
    if path is None:
        delete_cache()
    else:
        path = os.path.abspath(path)
        try:
            os.remove(os.path.join(path, 'phantomjs.exe'))
            print(os.path.join(path, 'phantomjs.exe'))
            for file in os.listdir(path):
                if 'phantomjs' in file and not os.path.isfile(file):
                    if 'phantomjs.exe' in os.listdir(os.path.join(path, file, 'bin')):
                        shutil.rmtree(os.path.join(path, file))
                        print(os.path.join(path, file))
                elif 'phantomjs' in file and file.endswith('.zip'):
                        os.remove(os.path.join(path, file))
                        print(os.path.join(path, file))
        except:
            pass

@pytest.mark.skipif(sys.platform != 'win32',
                    reason="run only on windows")
@pytest.mark.parametrize('path', [PATH, None])
def test_edge_manager_with_selenium(path):
    delete_old_install(path)
    driver_path = EdgeDriverManager().install(path)
    dr = webdriver.Edge(driver_path)
    dr.quit()


@pytest.mark.skipif(sys.platform != 'win32',
                    reason="run only on windows")
@pytest.mark.parametrize('path', [PATH, None])
def test_edge_manager_with_selenium_cache(path):
    driver_path = EdgeDriverManager().install(path)
    dr = webdriver.Edge(driver_path)
    dr.quit()


def test_can_download_edge_driver_binary():
    edge_driver = EdgeDriver("latest", "win")
    edge_driver_bin = cache.download_binary(edge_driver)
    assert edge_driver_bin.name == u'MicrosoftWebDriver'
    assert os.path.exists(edge_driver_bin.path)


def test_can_user_cached_edge_driver_binary():
    delete_cache()
    edge_driver = EdgeDriver("latest", "win")
    cache.download_binary(edge_driver)
    edge_driver_bin = cache.download_binary(edge_driver)
    assert edge_driver_bin.name == u'MicrosoftWebDriver'
    assert os.path.exists(edge_driver_bin.path)
