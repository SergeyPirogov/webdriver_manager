import os

import pytest

from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def log():
    os.environ['WDM_PRINT_FIRST_LINE'] = 'False'
    yield
    os.environ['WDM_PRINT_FIRST_LINE'] = 'True'


def test_chrome_manager_with_specific_version(log):
    bin = ChromeDriverManager("2.26").install()
    assert os.path.exists(bin)
