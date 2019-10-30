import datetime
import os
import platform
import re
import sys

import crayons
import requests


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


def validate_response(resp):
    if resp.status_code == 404:
        raise ValueError("There is no such driver by url {}".format(resp.url))
    elif resp.status_code != 200:
        raise ValueError(resp.json())


def write_file(content, path):
    with open(path, "wb") as code:
        code.write(content)
        code.close()
    return path


def download_driver(url):
    console("Trying to download new driver from {}".format(url))
    response = requests.get(url, stream=True)
    validate_response(response)
    return response


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
            'Could not get version for Chrome with this command: {}'
            .format(cmd)
        )
    return version.group(0)
