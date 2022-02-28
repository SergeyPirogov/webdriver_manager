import datetime
import base64
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


def validate_response(resp: requests.Response):
    if resp.status_code == 404:
        raise ValueError("There is no such driver by url {}".format(resp.url))
    elif resp.status_code != 200:
        raise ValueError(
            f'response body:\n{resp.text}\n'
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


def determine_powershell():
    """Returns "powershell" if process runs in CMD console."""
    cmd = '(dir 2>&1 *`|echo CMD);&<# rem #>echo powershell'
    with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True,
    ) as stream:
        stdout = stream.communicate()[0].decode()
    return '' if stdout == 'powershell' else 'powershell'

def linux_browser_apps_to_cmd(*apps: str) -> str:
    """Create 'browser --version' command from browser app names.

    Result command example:
        chromium --version || chromium-browser --version
    """
    ignore_errors_cmd_part = ' 2>/dev/null' if os.getenv('WDM_LOG_LEVEL') == '0' else ''
    return ' || '.join(f'{i} --version{ignore_errors_cmd_part}' for i in apps)


def windows_browser_apps_to_cmd(*apps: str) -> str:
    """Create analogue of browser --version command for windows.

    From browser paths and registry keys.

    Result command example:
       cmd1; if (-not $? -or $? -match $error) { cmd2 }
    """
    ignore_errors_cmd_part = ' 2>$null' if os.getenv('WDM_LOG_LEVEL') == '0' else ''
    powershell = determine_powershell()

    script = (
        "$ErrorActionPreference='silentlycontinue' ; "
            + f'{apps[0]}{ignore_errors_cmd_part} ;'
            + ''.join(f" if (-not $? -or $? -match $error) {{ {i}{ignore_errors_cmd_part} }}" for i in apps[1:])
    )

    b64script = str(base64.b64encode(script.encode("utf-16-le")), "utf-8")
    
    return f" {powershell} -EncodedCommand {b64script}"  
         

_CMD_MAPPING = {
    ChromeType.GOOGLE: {
        OSType.LINUX: ('google-chrome', 'google-chrome-stable', 'google-chrome-beta', 'google-chrome-dev'),
        OSType.MAC: r'/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version',
        OSType.WIN: (
            r'(Get-Item -Path "$env:PROGRAMFILES\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
            r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Google\Chrome\BLBeacon").version',
            r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome").version'
        ),
    },
    ChromeType.CHROMIUM: {
        OSType.LINUX: ('chromium', 'chromium-browser'),
        OSType.MAC: r'/Applications/Chromium.app/Contents/MacOS/Chromium --version',
        OSType.WIN: (
            r'(Get-Item -Path "$env:PROGRAMFILES\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:LOCALAPPDATA\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
            r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Chromium\BLBeacon").version',
            r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Chromium").version'
        ),
    },
    ChromeType.MSEDGE: {
        OSType.LINUX: ('microsoft-edge', 'microsoft-edge-stable', 'microsoft-edge-beta', 'microsoft-edge-dev'),
        OSType.MAC: r'/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version',
        OSType.WIN: (
            # stable edge
            r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge\BLBeacon").version',
            r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Microsoft\EdgeUpdate\Clients\{56EB18F8-8008-4CBD-B6D2-8C97FE7E9062}").pv',
            # beta edge
            r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge Beta\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge Beta\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge Beta\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge Beta\BLBeacon").version',
            # dev edge
            r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge Dev\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES\Microsoft\Edge Dev\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Microsoft\Edge Dev\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge Dev\BLBeacon").version',
            # canary edge
            r'(Get-Item -Path "$env:LOCALAPPDATA\Microsoft\Edge SxS\Application\msedge.exe").VersionInfo.FileVersion',
            r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Microsoft\Edge SxS\BLBeacon").version',
            # highest edge
            r"(Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe').'(Default)').VersionInfo.ProductVersion",
            r"[System.Diagnostics.FileVersionInfo]::GetVersionInfo((Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe').'(Default)').ProductVersion",
            r'Get-AppxPackage -Name *MicrosoftEdge.* | Foreach Version',
            r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge").version'
        ),
    },
    'firefox': {
        OSType.LINUX: ('firefox',),
        OSType.MAC: r'/Applications/Firefox.app/Contents/MacOS/firefox --version',
        OSType.WIN: (
            r'(Get-Item -Path "$env:PROGRAMFILES\Mozilla Firefox\firefox.exe").VersionInfo.FileVersion',
            r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Mozilla Firefox\firefox.exe").VersionInfo.FileVersion',
            r"(Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe').'(Default)').VersionInfo.ProductVersion",
            r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Mozilla\Mozilla Firefox").CurrentVersion'
        ),
    },
}

CMD_MAPPING_FUNCS = {
    OSType.LINUX: linux_browser_apps_to_cmd,
    OSType.WIN: windows_browser_apps_to_cmd,
    OSType.MAC: lambda x: x, # dummy function for mac
}

def get_command_to_read_browser_version(browser_type, os_name):
    """
    Get the command line command that can be executed to obtain 
    the browser version.

    Parameters
    ----------
    browser_type: str
        The used browser. Accepted values are ChromeType.GOOGLE,
        ChromeType.CHROMIUM, ChromeType.MSEDGE and "firefox".
    os_type: str
        The used operating system. Accepted values are OSType.WIN,
        OSType.MAC and OSType.LINUX.

    Returns
    -------
    cmd_string: str
        The command to run to obtain the browser version.

    Notes
    -----
        This function will also update the `webdriver_manager_utils.CMD_MAPPING` for the
        `browser_type` and `os_type` for caching purposes.
    """
    try: 
        cmd_string = _CMD_MAPPING[browser_type][os_name]
    except KeyError:
        return '' # will raise helpful error message later on.
    if not isinstance(cmd_string, str):
        cmd_string = CMD_MAPPING_FUNCS[os_name](cmd_string)
        # Caching: save the results to CMD_MAPPING
        _CMD_MAPPING[browser_type][os_name] = cmd_string
    return cmd_string


def get_browser_version_from_os(browser_type=None):
    """Return installed browser version."""
    pattern = (
        r'(\d+.\d+)'
        if browser_type == 'firefox'
        else r'\d+\.\d+\.\d+'
    )

    cmd = get_command_to_read_browser_version(browser_type, os_name())
    version = read_version_from_cmd(cmd, pattern)

    if not version:
        log(f'Could not get version for {browser_type} with the command: {cmd}')

    current_version = version.group(0) if version else 'UNKNOWN'

    log(f"Current {browser_type} version is {current_version}")

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
