import logging
import os

import pytest

from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def log():
    os.environ['WDM_LOG'] = str(logging.NOTSET)
    yield
    os.environ['WDM_LOG'] = str(logging.INFO)


def test_chrome_manager_with_specific_version(log):
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)
