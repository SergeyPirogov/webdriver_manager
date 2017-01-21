import logging

import requests

from webdriver_manager.config import Configuration


class Driver(object):
    def __init__(self, version, os_type):
        self.config = Configuration(section=self.__class__.__name__)
        self.config.set("version", version)
        self._url = self.config.url
        self.name = self.config.name
        self._version = self.config.version
        self.os_type = os_type

    def get_url(self):
        url = "{url}/{ver}/{name}_{os}.zip"
        return url.format(url=self._url,
                          ver=self.get_version(),
                          name=self.name,
                          os=self.os_type)

    def get_version(self):
        if self._version == "latest":
            return self.get_latest_release_version()
        return self._version

    def get_latest_release_version(self):
        raise NotImplementedError("Please implement this method")


class ChromeDriver(Driver):
    def __init__(self, version, os_type):
        super(ChromeDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        file = requests.get(self.config.driver_latest_release_url)
        return file.text.rstrip()


class GeckoDriver(Driver):
    def __init__(self, version, os_type):
        super(GeckoDriver, self).__init__(version, os_type)

    def get_latest_release_version(self):
        resp = requests.get(self.latest_release_url)
        self.validate_response(resp)
        return resp.json()["tag_name"]

    def get_url(self):
        # https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
        logging.warning(
            "Getting latest mozila release info for {0}".format(self.get_version()))
        resp = requests.get(self.tagged_release_url)
        self.validate_response(resp)
        assets = resp.json()["assets"]
        ver = self.get_version()
        name = "{0}-{1}-{2}".format(self.name, ver, self.os_type)
        output_dict = [asset for asset in assets if
                       asset['name'].startswith(name)]
        return output_dict[0]['browser_download_url']

    def validate_response(self, resp):
        if resp.status_code == 404:
            raise ValueError("There is no such driver {0} with version {1}".format(self.name,
                                                                                   self._version))
        elif resp.status_code != 200:
            raise ValueError(resp.json())

    @property
    def latest_release_url(self):
        token = self.config.gh_token
        url = self.config.driver_latest_release_url
        if token:
            return "{base_url}?access_token={access_token}".format(base_url=url,
                                                                   access_token=token)
        return url

    @property
    def tagged_release_url(self):
        token = self.config.gh_token
        url = self.config.mozila_release_tag.format(self.get_version())
        if token:
            return url + "?access_token={0}".format(token)
        return url


class EdgeDriver(Driver):
    def get_latest_release_version(self):
        return self.get_version()

    def __init__(self, version, os_type):
        super(EdgeDriver, self).__init__(version, os_type)

    def get_version(self):
        return self._version

    def get_url(self):
        return "{}/{}.exe".format(self._url, self.name)
