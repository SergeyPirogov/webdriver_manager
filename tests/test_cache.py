import os
import shutil
from time import sleep

from webdriver_manager import config
from webdriver_manager.cache import CacheManager

cache = CacheManager(to_folder=config.folder, dir_name=config.folder)

def delete_cache():
    cache_path = cache.get_cache_path()
    print("Delete cache folder {}".format(cache_path))
    if os.path.exists(cache_path):
        shutil.rmtree(cache_path)
    sleep(5)
