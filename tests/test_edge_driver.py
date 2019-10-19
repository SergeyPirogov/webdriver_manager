import os

import pytest

from webdriver_manager.microsoft import EdgeDriverManager


@pytest.mark.parametrize('path', [".", None])
def test_edge_manager_with_selenium_cache(path):
    driver_path = EdgeDriverManager(os_type="win32").install(path)
    assert os.path.exists(driver_path)
