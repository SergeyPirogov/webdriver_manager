import os
import sys
import tempfile

ROOT_FOLDER_NAME = ".wdm"
DEFAULT_PROJECT_ROOT_CACHE_PATH = os.path.join(sys.path[0], ROOT_FOLDER_NAME)


def get_default_user_home_cache_path():
    home = os.path.expanduser("~")
    if not home or home == os.path.sep or home.startswith("~"):
        home = tempfile.gettempdir()
    return os.path.join(home, ROOT_FOLDER_NAME)


DEFAULT_USER_HOME_CACHE_PATH = get_default_user_home_cache_path()
