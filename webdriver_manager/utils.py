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


def current_chrome_version():
    cmd_mapping = {OSType.LINUX: 'google-chrome --version',
                   OSType.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
                   OSType.WIN: r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'}

    cmd = cmd_mapping.get(os_name())
    if cmd is None:
        raise ValueError(
            'Could not get chrome version for {}'.format(os_name())
        )
    else:
        stdout = os.popen(cmd).read()
        version = re.findall(r'(\d+)\.*', stdout)
        return '.'.join(number for number in version)
