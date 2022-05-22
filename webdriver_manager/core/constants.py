import os
import sys

ROOT_FOLDER_NAME = ".wdm"
GH_TOKEN = os.getenv("GH_TOKEN", None)
WDM_SSL_VERIFY = os.getenv("WDM_SSL_VERIFY", True)
WDM_LOCAL = os.environ.get("WDM_LOCAL", "0")
DEFAULT_PROJECT_ROOT_CACHE_PATH = os.path.join(sys.path[0], ROOT_FOLDER_NAME)
DEFAULT_USER_HOME_CACHE_PATH = os.path.join(
    os.path.expanduser("~"), ROOT_FOLDER_NAME)
