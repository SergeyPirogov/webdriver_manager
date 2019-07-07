import os
import platform
import re
import sys

import crayons


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
    if platform.machine().endswith('64'):
        return 64
    else:
        return 32


def os_type():
    return os_name() + str(os_architecture())


def validate_response(self, resp):
    if resp.status_code == 404:
        raise ValueError(
            "There is no such driver {0} with version {1}".format(
                self.name, self._version))
    elif resp.status_code != 200:
        raise ValueError(resp.json())


def console(text, bold=False):
    print(crayons.yellow(text, bold=bold))


def chrome_version():
    pattern = r'\d+\.\d+\.\d+'
    cmd_mapping = {
        OSType.LINUX: 'google-chrome --version',
        OSType.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
        OSType.WIN: r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
    }

    cmd = cmd_mapping[os_name()]
    stdout = os.popen(cmd).read()
    version = re.search(pattern, stdout)
    if not version:
        raise ValueError(
            'Could not get version for Chrome with this command: {}'.format(cmd)
        )
    return version.group(0)
