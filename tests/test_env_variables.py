import os

import pytest

from webdriver_manager.driver import Driver


@pytest.mark.parametrize(
    'verify_value, expected_ssl_verify',
    [
        ('1', True),
        ('0', False),
        ('', True),
    ]
)
def test_driver_ssl_verify_env(verify_value, expected_ssl_verify):
    os.environ['WDM_SSL_VERIFY'] = verify_value

    assert Driver('a', 'b', 'c', 'd', 'e').ssl_verify is expected_ssl_verify
