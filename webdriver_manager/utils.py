import os
import platform
import sys

import tarfile
import zipfile


class Archive:
    def __init__(self):
        pass

    @staticmethod
    def extract_zip(zip_file, to_directory):
        zip = zipfile.ZipFile(zip_file)
        zip.extractall(to_directory)
        return zip.namelist()

    @staticmethod
    def extract_tar_file(tar_file, to_dir):
        tar = tarfile.open(tar_file.name, mode="r:gz")
        members = tar.getmembers()
        tar.extractall(to_dir)
        tar.close()
        return members

    @staticmethod
    def unpack(archive):
        to_directory = os.path.dirname(archive.name)
        if archive.name.endswith(".zip"):
            return Archive.extract_zip(archive, to_directory)
        else:
            file_list = Archive.extract_tar_file(archive, to_directory)
            return [x.name for x in file_list]


class OSUtils:
    @staticmethod
    def os_name():
        pl = sys.platform
        if pl == "linux" or pl == "linux2":
            return "linux"
        elif pl == "darwin":
            return "mac"
        elif pl == "win32":
            return "win"

    @staticmethod
    def os_architecture():
        bits = platform.architecture()[0]
        if bits == "64bit":
            return 64
        return 32

    @staticmethod
    def os_type():
        return OSUtils.os_name() + str(OSUtils.os_architecture())
