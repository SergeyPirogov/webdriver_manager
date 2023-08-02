import datetime
import os
import platform
import re
import subprocess
import sys

from tqdm import tqdm

from webdriver_manager.core.archive import Archive
from webdriver_manager.core.logger import log


class File(object):
    def __init__(self, stream):
        self.content = stream.content
        self.__stream = stream
        self.__temp_name = "driver"

    @property
    def filename(self) -> str:
        try:
            filename = re.findall(
                "filename=(.+)", self.__stream.headers["content-disposition"]
            )[0]
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
    if not os.path.exists(archive_path):
        raise FileExistsError(f"No file has been saved on such path {archive_path}")
    return Archive(archive_path, os_type=os_name())


class OSType(object):
    LINUX = "linux"
    MAC = "mac"
    WIN = "win"


class ChromeType(object):
    GOOGLE = "google-chrome"
    CHROMIUM = "chromium"
    BRAVE = "brave-browser"
    MSEDGE = "edge"


PATTERN = {
    ChromeType.CHROMIUM: r"\d+\.\d+\.\d+",
    ChromeType.GOOGLE: r"\d+\.\d+\.\d+",
    ChromeType.MSEDGE: r"\d+\.\d+\.\d+",
    "brave-browser": r"(\d+)",
    "firefox": r"(\d+.\d+)",
}


def os_name():
    pl = sys.platform
    if pl == "linux" or pl == "linux2":
        return OSType.LINUX
    elif pl == "darwin":
        return OSType.MAC
    elif pl == "win32":
        return OSType.WIN


def os_architecture():
    if platform.machine().endswith("64"):
        return 64
    else:
        return 32


def os_type():
    return f"{os_name()}{os_architecture()}"


def is_arch(os_sys_type):
    if '_m1' in os_sys_type:
        return True
    return platform.processor() != 'i386'


def is_mac_os(os_sys_type):
    return OSType.MAC in os_sys_type


def get_date_diff(date1, date2, date_format):
    a = datetime.datetime.strptime(date1, date_format)
    b = datetime.datetime.strptime(
        str(date2.strftime(date_format)), date_format)

    return (b - a).days


def linux_browser_apps_to_cmd(*apps: str) -> str:
    """Create 'browser --version' command from browser app names.

    Result command example:
        chromium --version || chromium-browser --version
    """
    ignore_errors_cmd_part = " 2>/dev/null" if os.getenv(
        "WDM_LOG_LEVEL") == "0" else ""
    return " || ".join(f"{i} --version{ignore_errors_cmd_part}" for i in apps)


def windows_browser_apps_to_cmd(*apps: str) -> str:
    """Create analogue of browser --version command for windows."""
    powershell = determine_powershell()

    first_hit_template = """$tmp = {expression}; if ($tmp) {{echo $tmp; Exit;}};"""
    script = "$ErrorActionPreference='silentlycontinue'; " + " ".join(
        first_hit_template.format(expression=e) for e in apps
    )

    return f'{powershell} -NoProfile "{script}"'


def get_browser_version_from_os(browser_type=None):
    """Return installed browser version."""
    cmd_mapping = {
        ChromeType.GOOGLE: {
            OSType.LINUX: linux_browser_apps_to_cmd(
                "google-chrome",
                "google-chrome-stable",
                "google-chrome-beta",
                "google-chrome-dev",
            ),
            OSType.MAC: r"/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --version",
            OSType.WIN: windows_browser_apps_to_cmd(
                r'(Get-Item -Path "$env:PROGRAMFILES\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Google\Chrome\BLBeacon").version',
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Google Chrome").version',
            ),
        },
        ChromeType.CHROMIUM: {
            OSType.LINUX: linux_browser_apps_to_cmd("chromium", "chromium-browser"),
            OSType.MAC: r"/Applications/Chromium.app/Contents/MacOS/Chromium --version",
            OSType.WIN: windows_browser_apps_to_cmd(
                r'(Get-Item -Path "$env:PROGRAMFILES\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:LOCALAPPDATA\Chromium\Application\chrome.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\Chromium\BLBeacon").version',
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Chromium").version',
            ),
        },
        ChromeType.BRAVE: {
            OSType.LINUX: linux_browser_apps_to_cmd(
                "brave-browser", "brave-browser-beta", "brave-browser-nightly"
            ),
            OSType.MAC: r"/Applications/Brave\ Browser.app/Contents/MacOS/Brave\ Browser --version",
            OSType.WIN: windows_browser_apps_to_cmd(
                r'(Get-Item -Path "$env:PROGRAMFILES\BraveSoftware\Brave-Browser\Application\brave.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\BraveSoftware\Brave-Browser\Application\brave.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\Application\brave.exe").VersionInfo.FileVersion',
                r'(Get-ItemProperty -Path Registry::"HKCU\SOFTWARE\BraveSoftware\Brave-Browser\BLBeacon").version',
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\BraveSoftware Brave-Browser").version',
            ),
        },
        ChromeType.MSEDGE: {
            OSType.LINUX: linux_browser_apps_to_cmd(
                "microsoft-edge",
                "microsoft-edge-stable",
                "microsoft-edge-beta",
                "microsoft-edge-dev",
            ),
            OSType.MAC: r"/Applications/Microsoft\ Edge.app/Contents/MacOS/Microsoft\ Edge --version",
            OSType.WIN: windows_browser_apps_to_cmd(
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
                r"Get-AppxPackage -Name *MicrosoftEdge.* | Foreach Version",
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall\Microsoft Edge").version',
            ),
        },
        "firefox": {
            OSType.LINUX: linux_browser_apps_to_cmd("firefox"),
            OSType.MAC: r"/Applications/Firefox.app/Contents/MacOS/firefox --version",
            OSType.WIN: windows_browser_apps_to_cmd(
                r'(Get-Item -Path "$env:PROGRAMFILES\Mozilla Firefox\firefox.exe").VersionInfo.FileVersion',
                r'(Get-Item -Path "$env:PROGRAMFILES (x86)\Mozilla Firefox\firefox.exe").VersionInfo.FileVersion',
                r"(Get-Item (Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\firefox.exe').'(Default)').VersionInfo.ProductVersion",
                r'(Get-ItemProperty -Path Registry::"HKLM\SOFTWARE\Mozilla\Mozilla Firefox").CurrentVersion',
            ),
        },
    }

    try:
        cmd_mapping = cmd_mapping[browser_type][os_name()]
        pattern = PATTERN[browser_type]
        version = read_version_from_cmd(cmd_mapping, pattern)
        return version
    except Exception:
        return None


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
        version = version.group(0) if version else None
    return version


def determine_powershell():
    """Returns "True" if runs in Powershell and "False" if another console."""
    cmd = "(dir 2>&1 *`|echo CMD);&<# rem #>echo powershell"
    with subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            stdin=subprocess.DEVNULL,
            shell=True,
    ) as stream:
        stdout = stream.communicate()[0].decode()
    return "" if stdout == "powershell" else "powershell"


def show_download_progress(response, _bytes_threshold=100):
    """ Opens up a response's content in chunks to show a progress bar with tqdm.
        Resets response._content when done so that response can be consumed again as normal. """
    total = int(response.headers.get("Content-Length", 0))
    if total > _bytes_threshold:
        content = bytearray()
        progress_bar = tqdm(desc="[WDM] - Downloading", total=total, unit_scale=True, unit_divisor=1024, unit="B")
        for chunk in response.iter_content(chunk_size=8192):
            if chunk:  # Filter out keep-alive new chunks
                progress_bar.update(len(chunk))
                content.extend(chunk)
        response._content = content  # To allow content to be "consumed" again
