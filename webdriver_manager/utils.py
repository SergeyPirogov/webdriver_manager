import datetime
import os
import platform
import re
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
    return Archive(archive_path)


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
        raise ValueError(resp.json())


def write_file(content, path):
    with open(path, "wb") as code:
        code.write(content)
    return path


def download_file(url: str) -> File:
    log(f"Trying to download new driver from {url}")
    response = requests.get(url, stream=True)
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


def chrome_version(browser_type=ChromeType.GOOGLE):
    pattern = r'\d+\.\d+\.\d+'

    cmd_mapping = {
        ChromeType.GOOGLE: {
            OSType.LINUX: 'google-chrome --version || google-chrome-stable --version',
            OSType.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
            OSType.WIN: r'reg query "HKEY_CURRENT_USER\Software\Google\Chrome\BLBeacon" /v version'
        },
        ChromeType.CHROMIUM: {
            OSType.LINUX: 'chromium --version || chromium-browser --version',
            OSType.MAC: r'/Applications/Chromium.app/Contents/MacOS/Chromium --version',
            OSType.WIN: r'reg query "HKEY_CURRENT_USER\Software\Chromium\BLBeacon" /v version'
        },
        ChromeType.MSEDGE: {
            OSType.MAC: r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version',
            OSType.WIN: r'reg query "HKEY_CURRENT_USER\SOFTWARE\Microsoft\Edge\BLBeacon" /v version',
        }
    }

    cmd = cmd_mapping[browser_type][os_name()]
    stdout = os.popen(cmd).read()
    version = re.search(pattern, stdout)
    if not version:
        raise ValueError(f'Could not get version for Chrome with this command: {cmd}')
    current_version = version.group(0)
    return current_version
