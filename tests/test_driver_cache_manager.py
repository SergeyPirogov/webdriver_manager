import json
import datetime

import requests

from webdriver_manager.core.driver_cache import DriverCacheManager
from webdriver_manager.firefox import GeckoDriverManager


class OSMock:
    def get_os_type(self):
        return "linux64"

    def get_browser_version_from_os(self, _browser_type):
        return "122.0"


class DriverMock:
    def __init__(self):
        self.version_lookup_calls = 0

    def get_name(self):
        return "geckodriver"

    def get_browser_type(self):
        return "firefox"

    def get_browser_version_from_os(self):
        return "122.0"

    def get_driver_version_to_download(self):
        self.version_lookup_calls += 1
        raise RuntimeError("remote lookup should not be called when cache already has matching browser version")


def test_find_driver_uses_cached_entry_without_remote_version_lookup(tmp_path):
    cache = DriverCacheManager(root_dir=str(tmp_path), os_system_manager=OSMock())
    driver = DriverMock()

    driver_dir = tmp_path / ".wdm" / "drivers" / "geckodriver" / "linux64" / "v0.34.0"
    driver_dir.mkdir(parents=True, exist_ok=True)
    binary_path = driver_dir / "geckodriver"
    binary_path.write_text("bin")

    metadata_path = tmp_path / ".wdm" / "drivers.json"
    metadata = {
        "linux64_geckodriver_v0.34.0_for_122.0": {
            "timestamp": datetime.date.today().strftime("%d/%m/%Y"),
            "binary_path": str(binary_path),
        }
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata))

    resolved_path = cache.find_driver(driver)

    assert resolved_path == str(binary_path)
    assert driver.version_lookup_calls == 0


def test_gecko_manager_install_uses_cache_without_network(monkeypatch, tmp_path):
    os_manager = OSMock()
    cache = DriverCacheManager(root_dir=str(tmp_path), os_system_manager=os_manager)

    driver_dir = tmp_path / ".wdm" / "drivers" / "geckodriver" / "linux64" / "v0.34.0"
    driver_dir.mkdir(parents=True, exist_ok=True)
    binary_path = driver_dir / "geckodriver"
    binary_path.write_text("bin")

    metadata_path = tmp_path / ".wdm" / "drivers.json"
    metadata = {
        "linux64_geckodriver_v0.34.0_for_122.0": {
            "timestamp": datetime.date.today().strftime("%d/%m/%Y"),
            "binary_path": str(binary_path),
        }
    }
    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata))

    network_calls = {"count": 0}

    def fail_requests_get(*args, **kwargs):
        network_calls["count"] += 1
        raise AssertionError("Network should not be called when cache contains a valid driver")

    monkeypatch.setattr(requests, "get", fail_requests_get)

    resolved_path = GeckoDriverManager(
        cache_manager=cache,
        os_system_manager=os_manager,
    ).install()

    assert resolved_path == str(binary_path)
    assert network_calls["count"] == 0
