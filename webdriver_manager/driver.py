import logging

import requests

import ff_config


class Driver(object):
    def __init__(self, driver_url, name, version, os_type):
        self._url = driver_url
        self.name = name
        self._version = version
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
    def __init__(self, driver_url, name, version, os_type):
        super(ChromeDriver, self).__init__(driver_url, name, version, os_type)

    def get_latest_release_version(self):
        file = requests.get(self._url + "/LATEST_RELEASE")
        return file.text.rstrip()


class FireFoxDriver(Driver):
    def __init__(self, driver_url, name, version, os_type):
        super(FireFoxDriver, self).__init__(driver_url, name, version, os_type)

    def get_latest_release_version(self):
        req_url = "{url}?access_token={access_token}".format(url=ff_config.mozila_latest_release,
                                                             access_token=ff_config.access_token)
        resp = requests.get(req_url)
        return resp.json()["tag_name"]

    def get_url(self):
        # https://github.com/mozilla/geckodriver/releases/download/v0.11.1/geckodriver-v0.11.1-linux64.tar.gz
        url = ff_config.mozila_release_tag.format(self.get_version())
        logging.warning(
            "Getting latest mozila release info {0}".format(url))
        resp = requests.get(url + "?access_token={0}".format(ff_config.access_token))

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
