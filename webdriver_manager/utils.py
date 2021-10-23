import datetime
import os
import platform
import re
import subprocess
import sys

import requests

from webdriver_manager.archive import Archive
from webdriver_manager.logger import log


class File(object):

    def __init__(self, stream):
        self.content = stream.content
        self.__stream = stream
        self.__temp_name = "driver"

    @property
    def filename(self) -> str:
        try:
            filename = re.findall("filename=(.+)", self.__stream.headers["content-disposition"])[0]
        except KeyError:
            filename = f"{self.__temp_name}.zip"
        except IndexError:
            filename = f"{self.__temp_name}.exe"

        if '"' in filename:
            filename = filename.replace('"', "")

        return filename


def save_file(file: File, directory: str):
    os.makedirs(directory, exist_ok=True)

    archive_path = f"{directory}{os.sep}{file.filename}"
    with open(archive_path, "wb") as code:
        code.write(file.content)
    return Archive(archive_path, os_type=os_name())


class OSType(object):
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


class ChromeType(object):
    GOOGLE = 'google-chrome'
    CHROMIUM = 'chromium'
    MSEDGE = 'edge'


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


def validate_response(resp):
    if resp.status_code == 404:
        raise ValueError("There is no such driver by url {}".format(resp.url))
    elif resp.status_code != 200:
        raise ValueError(
            f'response body:\n{resp.json()}\n'
            f'request url:\n{resp.request.url}\n'
            f'response headers:\n{dict(resp.headers)}\n'
        )


def write_file(content, path):
    with open(path, "wb") as code:
        code.write(content)
    return path


def download_file(url: str, ssl_verify=True) -> File:
    log(f"Trying to download new driver from {url}")
    response = requests.get(url, stream=True, verify=ssl_verify)
    validate_response(response)
    return File(response)


def get_date_diff(date1, date2, date_format):
    a = datetime.datetime.strptime(date1, date_format)
    b = datetime.datetime.strptime(str(date2.strftime(date_format)), date_format)

    return (b - a).days


def get_filename_from_response(response, name):
    try:
        filename = re.findall("filename=(.+)", response.headers["content-disposition"])[0]
    except KeyError:
        filename = "{}.zip".format(name)
    except IndexError:
        filename = name + ".exe"

    if '"' in filename:
        filename = filename.replace('"', "")

    return filename


def linux_browser_apps_to_cmd(*apps: str) -> str:
    """Create chrome version command from browser app names.

    Result command example:
        chromium --version || chromium-browser --version
    """
    ignore_errors_cmd_part = ' 2>/dev/null' if os.getenv('WDM_LOG_LEVEL') == '0' else ''
    return ' || '.join(list(map(lambda i: f'{i} --version{ignore_errors_cmd_part}', apps)))


def get_browser_version_from_os(browser_type=None):
    """Return installed browser version."""
    pattern = r'\d+\.\d+\.\d+'

    cmd_mapping = {
        ChromeType.GOOGLE: {
            OSType.LINUX: linux_browser_apps_to_cmd('google-chrome', 'google-chrome-stable'),
            OSType.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
            OSType.WIN: r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        },
        ChromeType.CHROMIUM: {
            OSType.LINUX: linux_browser_apps_to_cmd('chromium', 'chromium-browser'),
            OSType.MAC: r'/Applications/Chromium.app/Contents/MacOS/Chromium --version',
            OSType.WIN: r'reg query "HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome" /v version'
        },
        ChromeType.MSEDGE: {
            OSType.LINUX: linux_browser_apps_to_cmd('microsoft-edge', 'microsoft-edge-stable', 'microsoft-edge-beta', 'microsoft-edge-dev'),
            OSType.MAC: r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version',
            OSType.WIN: r'reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\BLBeacon" /v version',
        }
    }

    cmd = cmd_mapping[browser_type][os_name()]
    version = read_version_from_cmd(cmd, pattern)

    if not version:
        log(f'Could not get version for {browser_type} with the any command: {cmd}')

    current_version = version.group(0) if version else 'UNKNOWN'

    log(f"Current {browser_type} version is {current_version}")
    return current_version


def firefox_version():
    pattern = r'(\d+.\d+)'
    cmd_mapping = {
        OSType.LINUX: 'firefox --version',
        OSType.MAC: r'/Applications/Firefox.app/Contents/MacOS/firefox --version',
        OSType.WIN: r"Powershell (Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe').'(Default)').VersionInfo.ProductVersion",
    }
    cmd = cmd_mapping[os_name()]

    version = read_version_from_cmd(cmd, pattern)

    if not version:
        log(f'Could not get version for firefox with the any command: {cmd}')

    current_version = version.group(0) if version else 'UNKNOWN'

    log(f"Current firefox version is {current_version}")
    return current_version


def read_version_from_cmd(cmd, pattern):
    with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True,
    ) as stream:
        stdout = stream.communicate()[0].decode()
        version = re.search(pattern, stdout)
    return version
