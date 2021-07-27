import os
import tarfile
import zipfile
import typing


class LinuxZipFileWithPermissions(zipfile.ZipFile):
    """Class for extract files in linux with right permissions"""
    def extract(self, member, path=None, pwd=None):
        if not isinstance(member, zipfile.ZipInfo):
            member = self.getinfo(member)

        if path is None:
            path = os.getcwd()

        ret_val = self._extract_member(member, path, pwd)  # noqa
        attr = member.external_attr >> 16
        os.chmod(ret_val, attr)
        return ret_val


class Archive(object):

    def __init__(self, path: str, os_type: typing.Optional[str] = None):
        self.file_path = path
        self.os_type: typing.Optional[str] = os_type

    def unpack(self, directory):
        if self.file_path.endswith(".zip"):
            return self.__extract_zip(directory)
        elif self.file_path.endswith(".tar.gz"):
            return self.__extract_tar_file(directory)

    def __extract_zip(self, to_directory):
        zip_class = LinuxZipFileWithPermissions if self.os_type == "linux" else zipfile.ZipFile
        archive = zip_class(self.file_path)
        try:
            archive.extractall(to_directory)
        except Exception as e:
            if e.args[0] not in [26, 13] and e.args[1] not in ['Text file busy', 'Permission denied']:
                raise e
        return archive.namelist()

    def __extract_tar_file(self, to_directory):
        try:
            tar = tarfile.open(self.file_path, mode="r:gz")
        except tarfile.ReadError:
            tar = tarfile.open(self.file_path, mode="r:bz2")
        members = tar.getmembers()
        tar.extractall(to_directory)
        tar.close()
        return [x.name for x in members]
