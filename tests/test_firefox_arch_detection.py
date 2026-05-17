from webdriver_manager.firefox import GeckoDriverManager


class LinuxAarch64OsManagerMock:
    def get_os_type(self):
        return "linux64"

    def get_os_name(self):
        return "linux"

    def is_arch(self):
        return False

    def get_os_architecture(self):
        return 64

    @staticmethod
    def is_mac_os(_):
        return False


def test_gecko_manager_prefers_linux_aarch64_when_platform_reports_arm64(monkeypatch):
    monkeypatch.setattr("webdriver_manager.firefox.platform.machine", lambda: "aarch64")
    monkeypatch.setattr("webdriver_manager.firefox.platform.processor", lambda: "aarch64")

    manager = GeckoDriverManager(os_system_manager=LinuxAarch64OsManagerMock())

    assert manager.get_os_type() == "linux-aarch64"

