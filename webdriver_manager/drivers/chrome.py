from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import ChromeType, get_browser_version_from_os
import platform


class ChromeDriver(Driver):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client,
            chrome_type=ChromeType.GOOGLE,
    ):
        super(ChromeDriver, self).__init__(
            name, version, os_type, url, latest_release_url, http_client
        )
        self.chrome_type = chrome_type
        self.browser_version = ""

    def get_os_type(self):
        if "win" in super().get_os_type():
            return "win32"
        mac = f'{super().get_os_type()}' \
              f'{"_m1" if "mac" in super().get_os_type() and not platform.processor() == "i386" else ""}'
        return mac if "mac" in super().get_os_type() else super().get_os_type()

    def get_latest_release_version(self):
        self.browser_version = get_browser_version_from_os(self.chrome_type)
        log(f"Get LATEST {self._name} version for {self.browser_version} {self.chrome_type}")
        latest_release_url = (
            f"{self._latest_release_url}_{self.browser_version}"
            if self.browser_version
            else self._latest_release_url
        )
        resp = self._http_client.get(url=latest_release_url)
        self._version = resp.text.rstrip()
        return self._version
