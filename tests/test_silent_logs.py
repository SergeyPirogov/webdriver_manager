import os

import pytest

from webdriver_manager.chrome import ChromeDriverManager


def test_chrome_manager_with_logs_level_0_set_locally():
    bin = ChromeDriverManager("2.26", log_level=0).install()
    assert os.path.exists(bin)
