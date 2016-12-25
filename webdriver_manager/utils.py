import os
import platform
import sys

import tarfile
import zipfile

from webdriver_manager.binary import Binary


class Archive:
    def __init__(self):
        pass

    @staticmethod
    def extract_zip(zip_file, to_directory):
        zipfile.ZipFile(zip_file).extractall(to_directory)

    @staticmethod
    def extract_tar_file(tar_file, to_dir):
        tar = tarfile.open(tar_file.name, mode="r:gz")
        tar.extractall(to_dir)
        tar.close()

    @staticmethod
    def unpack(archive, filename):
        to_directory = os.path.dirname(archive.name)
        if archive.name.endswith(".zip"):
            Archive.extract_zip(archive, to_directory)
        else:
            Archive.extract_tar_file(archive, to_directory)
        return Binary(os.path.join(os.path.dirname(archive.name), filename))


class OSUtils:
    @staticmethod
    def os_name():
        pl = sys.platform
        if pl == "linux" or pl == "linux2":
            return "linux"
        elif pl == "darwin":
            return "mac"
        elif pl == "win32":
            return "windows"

    @staticmethod
    def os_architecture():
        bits = platform.architecture()[0]
        if bits == "64bit":
            return 64
        return 32
