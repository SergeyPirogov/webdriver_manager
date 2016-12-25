import logging

import requests

import config
from webdriver_manager.utils import OSUtils


class Driver(object):
    def __init__(self, driver_url, name, version):
        self._url = driver_url
        self.name = name
        self._version = version

    def get_url(self):
        url = "{url}/{ver}/{name}_{os}.zip"
        return url.format(url=self._url,
                          ver=self.get_version(),
                          name=self.name,
                          os=OSUtils.os_name() + str(OSUtils.os_architecture()))

    def get_version(self):
        if self._version == "latest":
            return self.get_latest_release_version()
        return self._version

    def get_latest_release_version(self):
        raise NotImplementedError("Please implement this method")


class ChromeDriver(Driver):
    def __init__(self, driver_url, name, version):
        super(ChromeDriver, self).__init__(driver_url, name, version)

    def get_latest_release_version(self):
        file = requests.get(self._url + "/LATEST_RELEASE")
        return file.text.rstrip()


class FireFoxDriver(Driver):
    def __init__(self, driver_url, name, version):
        super(FireFoxDriver, self).__init__(driver_url, name, version)

    def get_latest_release_version(self):
        resp = requests.get(config.mozila_latest_release)
        return resp.json()["tag_name"]

    def get_url(self):
        # https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
        url = config.mozila_release_tag.format(self.get_version())
        logging.warning(
            "Getting latest mozila release info {0}".format(url))
        resp = requests.get(url)
        if resp.status_code == 404:
            raise ValueError("There is no such driver {0} with version {1} by {2}".format(self.name,
                                                                                          self._version,
                                                                                          url))
        os = OSUtils.os_name() + str(OSUtils.os_architecture())
        assets = resp.json()["assets"]
        ver = self.get_version()
        name = "{0}-{1}-{2}".format(self.name, ver, os)
        output_dict = [asset for asset in assets if asset['name'].startswith(name)]
        return output_dict[0]['browser_download_url']
