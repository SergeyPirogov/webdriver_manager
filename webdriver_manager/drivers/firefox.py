from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log
from webdriver_manager.core.utils import get_browser_version_from_os, is_arch, is_mac_os


class GeckoDriver(Driver):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            mozila_release_tag,
            http_client
    ):
        super(GeckoDriver, self).__init__(
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client
        )
        self._mozila_release_tag = mozila_release_tag
        self.browser_version = ""

    def get_latest_release_version(self) -> str:
        self.browser_version = get_browser_version_from_os("firefox")
        log(f"Get LATEST {self._name} version for {self.browser_version} firefox")
        resp = self._http_client.get(
            url=self.latest_release_url,
            headers=self.auth_header
        )
        self._version = resp.json()["tag_name"]
        return self._version

    def get_url(self):
        """Like https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz"""
        log(f"Getting latest mozilla release info for {self.get_version()}")
        resp = self._http_client.get(
            url=self.tagged_release_url(self.get_version()),
            headers=self.auth_header
        )
        assets = resp.json()["assets"]
        name = f"{self.get_name()}-{self.get_version()}-{self.get_os_type()}."
        output_dict = [
            asset for asset in assets if asset["name"].startswith(name)]
        return output_dict[0]["browser_download_url"]

    def get_os_type(self):
        os_type = super().get_os_type()
        if not is_mac_os(os_type):
            return os_type

        macos = 'macos'
        if is_arch(os_type):
            return f"{macos}-aarch64"
        return macos

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def tagged_release_url(self, version):
        return self._mozila_release_tag.format(version)
