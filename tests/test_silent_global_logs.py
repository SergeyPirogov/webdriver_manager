import logging
import os

import pytest

from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def log():
    logging.getLogger('WDM').setLevel(logging.NOTSET)
    yield
    logging.getLogger('WDM').setLevel(logging.INFO)


def test_chrome_manager_with_specific_version(log):
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)
