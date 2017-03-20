from xml.etree import ElementTree as ET

import requests

from webdriver_manager import config
from webdriver_manager import utils
from webdriver_manager.config import Configuration
from webdriver_manager.utils import validate_response, OSType, console


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
            "Getting latest mozila release info for {0}".format(
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


class PhantomJsDriver(Driver):
    def __init__(self, version, os_type):
        # type: (str, str) -> None
        super(PhantomJsDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        # type: () -> str
        token = self.config.gh_token
        url = self.config.driver_tags_url
        if token:
            url = "{}?access_token={}".format(url, token)

        resp = requests.get(url=url)
        validate_response(self, resp)
        return resp.json()[0]['name']

    def get_url(self):
        # type: () -> str
        name = "{name}-{version}-{os}".format(name=self.name,
                                              version=self.get_version(),
                                              os=self.__file_name())
        return "{url}/{name}".format(url=self.config.url,
                                     name=name)

    def __file_name(self):
        # type: () -> str
        if self.os_type == OSType.MAC:
            return "macosx.zip"
        elif self.os_type == OSType.WIN:
            return "windows.zip"
        elif self.os_type == OSType.LINUX and utils.os_architecture() == 64:
            return "linux-x86_64.tar.bz2"
        elif self.os_type == OSType.LINUX and utils.os_architecture() == 32:
            return "linux-i686.tar.bz2"
        else:
            raise ValueError(
                "No such driver for os type {}".format(
                    utils.os_type()))


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
        root = ET.fromstring(resp.text)

        values = {}

        for child in root.findall(
                '{http://doc.s3.amazonaws.com/2006-03-01}Contents'):
            key = child.find(
                "{http://doc.s3.amazonaws.com/2006-03-01}Key").text
            if self.config.name in key:
                last_modified = child.find(
                    '{http://doc.s3.amazonaws.com/2006-03-01}LastModified').text
                values[last_modified] = key
        d = sorted(values, reverse=True)
        latest_release = values[d[0]]
        return latest_release[-9:-4]

    def __init__(self, version, os_type):
        # type: (str, str) -> None
        super(IEDriver, self).__init__(version, os_type)

    def get_url(self):
        # type: () -> str
        major, minor, patch = self.__get_divided_version()
        name = "{major}.{minor}/{name}_{os}_{major}.{minor}.{patch}.zip".format(
            name=self.name, os=self.os_type.capitalize(), major=major, minor=minor, patch=patch)
        return "{url}/{name}".format(url=self.config.url,
                                     name=name)

    def __get_divided_version(self):
        divided_version = self.get_version().split('.')
        if len(divided_version) == 2:
            return divided_version[0], divided_version[1], '0'
        elif len(divided_version) == 3:
            return divided_version
        else:
            raise ValueError(
                "Version must consist of major, minor and/or patch, but given was: {version}" .format(
                    version=self.get_version()))
