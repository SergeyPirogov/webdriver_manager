import pytest
from requests import Response, Request

from webdriver_manager.core.http import HttpClient


def test_validate_response_value_error_not_200_and_not_404():
    resp = Response()
    resp.headers = {}
    resp.request = Request()
    resp.request.url = "https://example.com"
    resp.status_code = 301
    resp._content = b"abc"

    with pytest.raises(ValueError) as excinfo:
        HttpClient.validate_response(resp)

    assert str(excinfo.value) == "\n".join(
        [
            "response body:",
            "abc",
            "request url:",
            "https://example.com",
            "response headers:",
            "{}",
            ""
        ]
    )


def test_validate_response_value_error_404():
    resp = Response()
    resp.request = Request()
    resp.url = "https://example.com"
    resp.status_code = 404

    with pytest.raises(ValueError) as excinfo:
        HttpClient.validate_response(resp)

    expected_message = "There is no such driver by url https://example.com"
    assert str(excinfo.value) == expected_message
