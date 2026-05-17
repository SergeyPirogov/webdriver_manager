import tempfile
import os

from webdriver_manager.core.constants import ROOT_FOLDER_NAME, get_default_user_home_cache_path
from webdriver_manager.core.constants import get_default_project_root_cache_path


def test_default_user_home_cache_path_falls_back_to_temp_if_home_is_root(monkeypatch):
    monkeypatch.setattr("os.path.expanduser", lambda _path: "/")

    cache_path = get_default_user_home_cache_path()

    assert cache_path == os.path.join(tempfile.gettempdir(), ROOT_FOLDER_NAME)


def test_default_user_home_cache_path_falls_back_to_temp_if_home_is_unresolved(monkeypatch):
    monkeypatch.setattr("os.path.expanduser", lambda _path: "~")

    cache_path = get_default_user_home_cache_path()

    assert cache_path == os.path.join(tempfile.gettempdir(), ROOT_FOLDER_NAME)


def test_default_project_root_cache_path_uses_cwd_for_frozen_app(monkeypatch):
    monkeypatch.setattr("sys.path", ["C:/app/base_library.zip"])
    monkeypatch.setattr("sys.frozen", True, raising=False)
    monkeypatch.setattr("os.getcwd", lambda: "C:/app/runtime")

    cache_path = get_default_project_root_cache_path()

    assert cache_path == os.path.join("C:/app/runtime", ROOT_FOLDER_NAME)
