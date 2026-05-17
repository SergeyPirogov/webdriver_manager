from webdriver_manager.core.manager import DriverManager


class FakeCacheManager:
    def __init__(self):
        self.find_calls = 0
        self.saved = False

    def find_driver(self, _driver):
        self.find_calls += 1
        if self.find_calls == 1:
            return None
        return "/tmp/cached/chromedriver"

    def get_driver_lock_path(self, _driver_name, _os_type):
        return "/tmp/wdm-test-lock"

    def save_file_to_cache(self, _driver, _file):
        self.saved = True
        return "/tmp/new/chromedriver"


class FakeDownloadManager:
    def __init__(self):
        self.download_calls = 0
        self.http_client = None

    def download_file(self, _url):
        self.download_calls += 1
        return object()


class FakeDriver:
    def get_name(self):
        return "chromedriver"

    def get_driver_download_url(self, _os_type):
        return "https://example.invalid/chromedriver.zip"

    def get_browser_type(self):
        return "google-chrome"


class FakeOSManager:
    def get_os_type(self):
        return "linux64"


def test_get_driver_binary_path_rechecks_cache_after_lock(monkeypatch):
    cache = FakeCacheManager()
    downloader = FakeDownloadManager()
    manager = DriverManager(
        download_manager=downloader,
        cache_manager=cache,
        os_system_manager=FakeOSManager(),
    )

    monkeypatch.setattr(DriverManager, "_acquire_lock", staticmethod(lambda _path, timeout=60.0, poll_interval=0.1: 1))
    monkeypatch.setattr(DriverManager, "_release_lock", staticmethod(lambda _fd, _path: None))

    path = manager._get_driver_binary_path(FakeDriver())

    assert path == "/tmp/cached/chromedriver"
    assert cache.find_calls == 2
    assert downloader.download_calls == 0
    assert cache.saved is False
