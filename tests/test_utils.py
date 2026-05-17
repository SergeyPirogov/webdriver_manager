import pytest
from requests import Response, Request
import base64

from webdriver_manager.core.http import HttpClient
from webdriver_manager.core.utils import windows_browser_apps_to_cmd


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


def test_windows_browser_apps_to_cmd_uses_encoded_command(monkeypatch):
    monkeypatch.setattr("webdriver_manager.core.utils.determine_powershell", lambda: "powershell")
    expression = r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge\Application\msedge.exe").VersionInfo.FileVersion'

    cmd = windows_browser_apps_to_cmd(expression)

    assert " -EncodedCommand " in cmd
    encoded = cmd.split(" -EncodedCommand ", 1)[1]
    script = base64.b64decode(encoded).decode("utf-16le")
    assert expression in script
    assert "$ErrorActionPreference='silentlycontinue';" in script
