from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log


class OperaDriver(Driver):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            opera_release_tag,
            http_client):
        super(OperaDriver, self).__init__(
            name, version, os_type, url, latest_release_url, http_client
        )
        self.opera_release_tag = opera_release_tag

    def get_latest_release_version(self) -> str:
        resp = self._http_client.get(
            url=self.latest_release_url,
            headers=self.auth_header
        )
        self._version = resp.json()["tag_name"]
        return self._version

    def get_url(self) -> str:
        # https://github.com/operasoftware/operachromiumdriver/releases/download/v.2.45/operadriver_linux64.zip
        version = self.get_version()
        log(f"Getting latest opera release info for {version}")
        resp = self._http_client.get(
            url=self.tagged_release_url(version),
            headers=self.auth_header
        )
        assets = resp.json()["assets"]
        name = "{0}_{1}".format(self.get_name(), self.get_os_type())
        output_dict = [
            asset for asset in assets if asset["name"].startswith(name)]
        return output_dict[0]["browser_download_url"]

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def tagged_release_url(self, version):
        return self.opera_release_tag.format(version)

    def get_browser_type(self):
        return "opera"

    def get_browser_version(self):
        try:
            return super().get_browser_version()
        except:
            return "latest"