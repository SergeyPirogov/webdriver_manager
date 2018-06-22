import re
from xml.etree import ElementTree

import requests

from webdriver_manager import config
from webdriver_manager.config import Configuration
from webdriver_manager.utils import validate_response, console


class Driver(object):
    def __init__(self, version, os_type):
        # type: (str, str) -> None
        self.config = Configuration(file_name=config.filename,
                                    config_folder=config.folder,
                                    section=self.__class__.__name__)
        self.config.set("version", version)
        self._url = self.config.url
        self.name = self.config.name
        self._version = self.config.version
        self.os_type = os_type

    def get_url(self):
        # type: () -> str
        url = "{url}/{ver}/{name}_{os}.zip"
        return url.format(url=self._url,
                          ver=self.get_version(),
                          name=self.name,
                          os=self.os_type)

    def get_version(self):
        # type: () -> str
        if self._version == "latest":
            return self.get_latest_release_version()
        return self._version

    def get_latest_release_version(self):
        # type: () -> str
        raise NotImplementedError("Please implement this method")


class ChromeDriver(Driver):
    def __init__(self, version, os_type):
        # type: (str, str) -> ChromeDriver
        super(ChromeDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        # type: () -> str
        file = requests.get(self.config.driver_latest_release_url)
        return file.text.rstrip()


class GeckoDriver(Driver):
    def __init__(self, version, os_type):
        # type: (str, str) -> None
        super(GeckoDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        # type: () -> str
        resp = requests.get(self.latest_release_url)
        validate_response(self, resp)
        return resp.json()["tag_name"]

    def get_url(self):
        # type: () -> str
        # https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
        console(
            "Getting latest mozilla release info for {0}".format(
                self.get_version()))
        resp = requests.get(self.tagged_release_url)
        validate_response(self, resp)
        assets = resp.json()["assets"]
        ver = self.get_version()
        name = "{0}-{1}-{2}".format(self.name, ver, self.os_type)
        output_dict = [asset for asset in assets if
                       asset['name'].startswith(name)]
        return output_dict[0]['browser_download_url']

    @property
    def latest_release_url(self):
        # type: () -> str
        token = self.config.gh_token
        url = self.config.driver_latest_release_url
        if token:
            return "{base_url}?access_token={access_token}".format(
                base_url=url, access_token=token)
        return url

    @property
    def tagged_release_url(self):
        # type: () -> str
        token = self.config.gh_token
        url = self.config.mozila_release_tag.format(self.get_version())
        if token:
            return url + "?access_token={0}".format(token)
        return url


class EdgeDriver(Driver):
    def get_latest_release_version(self):
        # type: () -> str
        return self.get_version()

    def __init__(self, version, os_type):
        # type: (str, str) -> None
        super(EdgeDriver, self).__init__(version, os_type)

    def get_version(self):
        # type: () -> str
        return self._version

    def get_url(self):
        # type: () -> str
        return "{}/{}.exe".format(self._url, self.name)


class IEDriver(Driver):
    def sortchildrenby(self, container):
        data = []
        for elem in container.iter("Contents"):
            key = elem
            data.append((key, elem))

        data.sort()

    def get_latest_release_version(self):
        # type: () -> str
        url = self.config.url
        resp = requests.get(url)
        root = ElementTree.fromstring(resp.text)

        values = {}

        xmlns = '{http://doc.s3.amazonaws.com/2006-03-01}'

        for child in root.findall(xmlns + 'Contents'):
            key = child.find(xmlns + 'Key').text
            if self.config.name in key and self.os_type in key:
                last_modified = child.find(xmlns + 'LastModified').text
                values[last_modified] = key

        latest_key = values[max(values)]
        # 2.39/IEDriverServer_Win32_2.39.0.zip
        m = re.match(r".*_{os}_(.*)\.zip".format(os=self.os_type), latest_key)
        if m:
            return m.group(1)
        else:
            raise ValueError("Can't parse latest version {key} | {os}".format(
                key=latest_key, os=self.os_type))

    def __init__(self, version, os_type):
        # type: (str, str) -> None
        if os_type == "win64":
            os_type = "x64"
        else:
            os_type = "Win32"
        super(IEDriver, self).__init__(version, os_type)

    def get_url(self):
        # type: () -> str
        major, minor, patch = self.__get_divided_version()
        return ("{url}/{major}.{minor}/"
                "{name}_{os}_{major}.{minor}.{patch}.zip").format(
                    url=self.config.url, name=self.name, os=self.os_type,
                    major=major, minor=minor, patch=patch)

    def __get_divided_version(self):
        divided_version = self.get_version().split('.')
        if len(divided_version) == 2:
            return divided_version[0], divided_version[1], '0'
        elif len(divided_version) == 3:
            return divided_version
        else:
            raise ValueError(
                "Version must consist of major, minor and/or patch, "
                "but given was: {version}".format(version=self.get_version()))
