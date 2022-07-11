from webdriver_manager.core.driver import Driver
from webdriver_manager.core.logger import log


class IEDriver(Driver):

    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            ie_release_tag,
            http_client
    ):
        super(IEDriver, self).__init__(
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client
        )
        self.os_type = "x64" if os_type == "win64" else "Win32"
        self._ie_release_tag = ie_release_tag
        # todo: for 'browser_version' implement installed IE version detection
        #       like chrome or firefox

    def get_latest_release_version(self) -> str:
        log(f"Get LATEST driver version for {self.get_browser_version()}")
        resp = self._http_client.get(
            url=self.latest_release_url,
            headers=self.auth_header
        )

        releases = resp.json()
        release = next(
            release
            for release in releases
            for asset in release["assets"]
            if asset["name"].startswith(self.get_name())
        )
        self._version = release["tag_name"].replace("selenium-", "")
        return self._version

    def get_url(self):
        """Like https://github.com/seleniumhq/selenium/releases/download/3.141.59/IEDriverServer_Win32_3.141.59.zip"""
        log(f"Getting latest ie release info for {self.get_version()}")
        resp = self._http_client.get(
            url=self.tagged_release_url(self.get_version()),
            headers=self.auth_header
        )

        assets = resp.json()["assets"]

        name = f"{self.get_name()}_{self.os_type}_{self.get_version()}" + "."
        output_dict = [
            asset for asset in assets if asset["name"].startswith(name)]
        return output_dict[0]["browser_download_url"]

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def tagged_release_url(self, version):
        version = self.__get_divided_version(version)
        return self._ie_release_tag.format(version)

    def __get_divided_version(self, version):
        divided_version = version.split(".")
        if len(divided_version) == 2:
            return f"{version}.0"
        elif len(divided_version) == 3:
            return version
        else:
            raise ValueError(
                "Version must consist of major, minor and/or patch, "
                "but given was: '{version}'".format(version=version)
            )

    def get_browser_type(self):
        return "msie"

    def get_browser_version(self):
        try:
            return super().get_browser_version()
        except:
            return "latest"
