import platform
import sys


class OSType(object):
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


def os_name():
    pl = sys.platform
    if pl == "linux" or pl == "linux2":
        return OSType.LINUX
    elif pl == "darwin":
        return OSType.MAC
    elif pl == "win32":
        return OSType.WIN


def os_architecture():
    bits = platform.architecture()[0]
    if bits == "64bit":
        return 64
    return 32


def os_type():
    return os_name() + str(os_architecture())


def validate_response(self, resp):
    if resp.status_code == 404:
        raise ValueError("There is no such driver {0} with version {1}".format(self.name,
                                                                               self._version))
    elif resp.status_code != 200:
        raise ValueError(resp.json())
