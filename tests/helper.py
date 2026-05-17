import json

from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.drivers.chrome import ChromeDriver


class ResponseMock:
    def __init__(self, body):
        self.body = body
        self.text = body if isinstance(body, str) else json.dumps(body)

    def json(self):
        if isinstance(self.body, str):
            return json.loads(self.body)
        return self.body


class HttpClientMock:
    def __init__(self, responses):
        self.responses = responses
        self.requested_urls = []

    def get(self, url, **kwargs):
        self.requested_urls.append(url)
        return ResponseMock(self.responses[url])


class OperationSystemManagerMock:
    def __init__(self, browser_version):
        self.browser_version = browser_version

    def get_browser_version_from_os(self, browser_type=None):
        return self.browser_version


def chrome_driver_for(browser_version, responses, chrome_type=ChromeType.CHROMIUM):
    http_client = HttpClientMock(responses)
    driver = ChromeDriver(
        name="chromedriver",
        driver_version=None,
        url="https://storage.googleapis.com/chrome-for-testing-public/",
        latest_release_url=(
            "https://googlechromelabs.github.io/chrome-for-testing/LATEST_RELEASE_STABLE"
        ),
        http_client=http_client,
        os_system_manager=OperationSystemManagerMock(browser_version),
        chrome_type=chrome_type,
    )
    return driver, http_client
