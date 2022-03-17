import os
import platform

import requests

from webdriver_manager.logger import log
from webdriver_manager.utils import (
    validate_response,
    get_browser_version_from_os,
    ChromeType,
    OSType,
)


class Driver(object):
    def __init__(self, name,
                 version,
                 os_type,
                 url,
                 latest_release_url):
        self._name = name
        self._url = url
        self._version = version
        self._os_type = os_type
        self._latest_release_url = latest_release_url
        self.ssl_verify = False if os.getenv('WDM_SSL_VERIFY') == '0' else True

    def get_name(self):
        return self._name

    def get_os_type(self):
        return self._os_type

    def get_url(self):
        return f"{self._url}/{self.get_version()}/{self.get_name()}_{self.get_os_type()}.zip"

    def get_version(self):
        self._version = (
            self.get_latest_release_version()
            if self._version == "latest"
            else self._version
        )
        return self._version

    def get_latest_release_version(self):
        # type: () -> str
        raise NotImplementedError("Please implement this method")


class ChromeDriver(Driver):
    def __init__(self, name, version, os_type, url, latest_release_url,
                 chrome_type=ChromeType.GOOGLE):
        super(ChromeDriver, self).__init__(name, version, os_type, url,
                                           latest_release_url)
        self.chrome_type = chrome_type
        self.browser_version = ""

    def get_os_type(self):
        if "win" in super().get_os_type():
            return "win32"
        mac = f'{super().get_os_type()}{"_m1" if "mac" in super().get_os_type() and not platform.processor() == "i386" else ""}'
        return mac if 'mac' in super().get_os_type() else super().get_os_type()

    def get_latest_release_version(self):
        self.browser_version = get_browser_version_from_os(self.chrome_type)
        log(f"Get LATEST {self._name} version for {self.browser_version} {self.chrome_type}")
        latest_release_url = (
            f"{self._latest_release_url}_{self.browser_version}"
            if self.browser_version
            else self._latest_release_url
        )
        resp = requests.get(
            url=latest_release_url,
            verify=self.ssl_verify
        )
        validate_response(resp)
        self._version = resp.text.rstrip()
        return self._version


class GeckoDriver(Driver):
    def __init__(
        self,
        name,
        version,
        os_type,
        url,
        latest_release_url,
        mozila_release_tag,
    ):
        super(GeckoDriver, self).__init__(
            name,
            version,
            os_type,
            url,
            latest_release_url,
        )
        self._mozila_release_tag = mozila_release_tag
        self.browser_version = ""
        self._os_token = os.getenv("GH_TOKEN", None)
        self.auth_header = (
            {'Authorization': f'token {self._os_token}'}
            if self._os_token
            else None
        )
        if self._os_token:
            log("GH_TOKEN will be used to perform requests", first_line=True)

    def get_latest_release_version(self) -> str:
        self.browser_version = get_browser_version_from_os("firefox")
        log(f"Get LATEST {self._name} version for {self.browser_version} firefox")
        resp = requests.get(
            url=self.latest_release_url,
            headers=self.auth_header,
            verify=self.ssl_verify,
        )
        validate_response(resp)
        self._version = resp.json()["tag_name"]
        return self._version

    def get_url(self):
        """Like https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz"""
        log(f"Getting latest mozilla release info for {self.get_version()}")
        resp = requests.get(
            url=self.tagged_release_url(self.get_version()),
            headers=self.auth_header,
            verify=self.ssl_verify,
        )
        validate_response(resp)
        assets = resp.json()["assets"]

        name = f"{self.get_name()}-{self.get_version()}-{self.get_os_type()}."
        output_dict = [
            asset for asset in assets if asset['name'].startswith(name)
        ]
        return output_dict[0]['browser_download_url']

    def get_os_type(self):
        mac = f'macos{"-aarch64" if platform.processor() != "i386" else ""}'
        return mac if 'mac' in super().get_os_type() else super().get_os_type()

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def tagged_release_url(self, version):
        return self._mozila_release_tag.format(version)


class IEDriver(Driver):
    def __init__(
        self,
        name,
        version,
        os_type,
        url,
        latest_release_url,
        ie_release_tag,
    ):
        super(IEDriver, self).__init__(
            name,
            version,
            os_type,
            url,
            latest_release_url,
        )
        self.os_type = "x64" if os_type == "win64" else "Win32"
        self._ie_release_tag = ie_release_tag
        # todo: for 'browser_version' implement installed IE version detection
        #       like chrome or firefox
        self.browser_version = ""
        self._os_token = os.getenv("GH_TOKEN", None)
        self.auth_header = (
            {'Authorization': f'token {self._os_token}'}
            if self._os_token
            else None
        )
        if self._os_token:
            log("GH_TOKEN will be used to perform requests", first_line=True)

    def get_latest_release_version(self) -> str:
        log(f"Get LATEST driver version for {self.browser_version}")
        resp = requests.get(
            url=self.latest_release_url,
            headers=self.auth_header,
            verify=self.ssl_verify,
        )
        validate_response(resp)
        releases = resp.json()
        release = next(
            release
            for release in releases
            for asset in release['assets']
            if asset['name'].startswith(self.get_name())
        )
        self._version = release['tag_name'].replace('selenium-', '')
        return self._version

    def get_url(self):
        """Like https://github.com/seleniumhq/selenium/releases/download/3.141.59/IEDriverServer_Win32_3.141.59.zip"""
        log(f"Getting latest ie release info for {self.get_version()}")
        resp = requests.get(
            url=self.tagged_release_url(self.get_version()),
            headers=self.auth_header,
            verify=self.ssl_verify,
        )
        validate_response(resp)
        assets = resp.json()["assets"]

        name = f"{self.get_name()}_{self.os_type}_{self.get_version()}" + "."
        output_dict = [
            asset for asset in assets if asset['name'].startswith(name)
        ]
        return output_dict[0]['browser_download_url']

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def tagged_release_url(self, version):
        version = self.__get_divided_version(version)
        return self._ie_release_tag.format(version)

    def __get_divided_version(self, version):
        divided_version = version.split('.')
        if len(divided_version) == 2:
            return f'{version}.0'
        elif len(divided_version) == 3:
            return version
        else:
            raise ValueError(
                "Version must consist of major, minor and/or patch, "
                "but given was: {version}".format(version=self.get_version())
            )


class OperaDriver(Driver):
    def __init__(self, name,
                 version,
                 os_type,
                 url,
                 latest_release_url,
                 opera_release_tag):
        super(OperaDriver, self).__init__(name, version, os_type, url,
                                          latest_release_url)
        self.opera_release_tag = opera_release_tag
        self._os_token = os.getenv("GH_TOKEN", None)
        self.auth_header = None
        self.browser_version = ""
        if self._os_token:
            log("GH_TOKEN will be used to perform requests")
            self.auth_header = {'Authorization': f'token {self._os_token}'}

    def get_latest_release_version(self) -> str:
        resp = requests.get(
            url=self.latest_release_url,
            headers=self.auth_header,
            verify=self.ssl_verify,
        )
        validate_response(resp)
        self._version = resp.json()["tag_name"]
        return self._version

    def get_url(self) -> str:
        # https://github.com/operasoftware/operachromiumdriver/releases/download/v.2.45/operadriver_linux64.zip
        version = self.get_version()
        log(f"Getting latest opera release info for {version}")
        resp = requests.get(
            url=self.tagged_release_url(version),
            headers=self.auth_header,
            verify=self.ssl_verify,
        )
        validate_response(resp)
        assets = resp.json()["assets"]
        name = "{0}_{1}".format(self.get_name(), self.get_os_type())
        output_dict = [asset for asset in assets if
                       asset['name'].startswith(name)]
        return output_dict[0]['browser_download_url']

    @property
    def latest_release_url(self):
        return self._latest_release_url

    def tagged_release_url(self, version):
        return self.opera_release_tag.format(version)


class EdgeChromiumDriver(Driver):
    def __init__(
        self,
        name,
        version,
        os_type,
        url,
        latest_release_url,
    ):
        super(EdgeChromiumDriver, self).__init__(
            name,
            version,
            os_type,
            url,
            latest_release_url,
        )
        self.browser_version = ""

    def get_stable_release_version(self):
        """Stable driver version when browser version was not determined."""
        stable = self._latest_release_url.replace('LATEST_RELEASE', 'LATEST_STABLE')
        resp = requests.get(stable, verify=self.ssl_verify)
        validate_response(resp)
        return resp.text.rstrip()

    def get_latest_release_version(self) -> str:
        browser_version = get_browser_version_from_os(ChromeType.MSEDGE)
        self.browser_version = (
            browser_version
            if browser_version
            else self.get_stable_release_version()
        )
        log(f"Get LATEST {self._name} version for {self.browser_version} Edge")
        major_edge_version = self.browser_version.split(".")[0]
        latest_release_url = {
            OSType.WIN in self.get_os_type(): f'{self._latest_release_url}_{major_edge_version}_WINDOWS',
            OSType.MAC in self.get_os_type(): f'{self._latest_release_url}_{major_edge_version}_MACOS',
            OSType.LINUX in self.get_os_type(): f'{self._latest_release_url}_{major_edge_version}_LINUX',
        }[True]
        resp = requests.get(latest_release_url, verify=self.ssl_verify)
        validate_response(resp)
        self._version = resp.text.rstrip()
        return self._version
