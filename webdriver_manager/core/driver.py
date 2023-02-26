from webdriver_manager.core import utils
from webdriver_manager.core.logger import log
from webdriver_manager.core.config import gh_token
from webdriver_manager.core.utils import get_browser_version_from_os


class Driver(object):
    def __init__(
            self,
            name,
            version,
            os_type,
            url,
            latest_release_url,
            http_client):
        self._name = name
        self._url = url
        self._version = version
        self._os_type = os_type
        if os_type is None:
            self._os_type = utils.os_type()
        self._latest_release_url = latest_release_url
        self._http_client = http_client
        self._browser_version = None
        self._driver_to_download_version = None

    @property
    def auth_header(self):
        token = gh_token()
        if token:
            log("GH_TOKEN will be used to perform requests")
            return {"Authorization": f"token {token}"}
        return None

    def get_name(self):
        return self._name

    def get_os_type(self):
        return self._os_type

    def get_driver_download_url(self):
        return f"{self._url}/{self.get_driver_version_to_download()}/{self._name}_{self._os_type}.zip"

    def get_driver_version_to_download(self):
        """
        Downloads version from parameter if version not None or "latest".
        Downloads latest, if version is "latest" or browser could not been determined.
        Downloads determined browser version driver in all other ways as a bonus fallback for lazy users.
        """
        if not self._driver_to_download_version:
            self._driver_to_download_version = self._version if self._version not in (None, "latest") else self.get_latest_release_version()
        return self._driver_to_download_version

    def get_latest_release_version(self):
        # type: () -> str
        raise NotImplementedError("Please implement this method")

    def get_browser_version_from_os(self):
        """
        Use-cases:
        - for key in metadata;
        - for printing nice logs;
        - for fallback if version was not set at all.
        Note: the fallback may have collisions in user cases when previous browser was not uninstalled properly.
        """
        if self._browser_version is None:
            self._browser_version = get_browser_version_from_os(self.get_browser_type())
        return self._browser_version

    def get_browser_type(self):
        raise NotImplementedError("Please implement this method")

    def get_binary_name(self):
        driver_name = self.get_name()
        driver_binary_name = (
            "msedgedriver" if driver_name == "edgedriver" else driver_name
        )
        driver_binary_name = (
            f"{driver_binary_name}.exe" if "win" in self.get_os_type() else driver_binary_name
        )
        return driver_binary_name
