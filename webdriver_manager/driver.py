import requests

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
        raise NotImplementedError()


class ChromeDriver(Driver):
    def __init__(self, driver_url, name, version):
        super(ChromeDriver, self).__init__(driver_url=driver_url,
                                           name=name,
                                           version=version)

    def get_latest_release_version(self):
        file = requests.get(self._url + "/LATEST_RELEASE")
        return file.text.rstrip()


    def get_version(self):
        if self._version == "latest":
            return self.get_latest_release_version()
        return self._version
