import tempfile

from webdriver_manager.core.constants import ROOT_FOLDER_NAME, get_default_user_home_cache_path


def test_default_user_home_cache_path_falls_back_to_temp_if_home_is_root(monkeypatch):
    monkeypatch.setattr("os.path.expanduser", lambda _path: "/")

    cache_path = get_default_user_home_cache_path()

    assert cache_path == f"{tempfile.gettempdir()}/{ROOT_FOLDER_NAME}"


def test_default_user_home_cache_path_falls_back_to_temp_if_home_is_unresolved(monkeypatch):
    monkeypatch.setattr("os.path.expanduser", lambda _path: "~")

    cache_path = get_default_user_home_cache_path()

    assert cache_path == f"{tempfile.gettempdir()}/{ROOT_FOLDER_NAME}"
