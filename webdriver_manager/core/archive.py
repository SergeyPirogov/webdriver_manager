import os
import io
import typing
import tarfile
import zipfile
import arpy
import lzma

from gzip import GzipFile

import zstandard


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
        elif self.file_path.endswith(".deb"):
            return self.__extract_deb_file(directory)
        else:
            raise Exception('unrecognized archive file type')

    def __extract_zip(self, to_directory):
        zip_class = (LinuxZipFileWithPermissions if self.os_type ==
                     "linux" else zipfile.ZipFile)
        archive = zip_class(self.file_path)
        try:
            archive.extractall(to_directory)
        except Exception as e:
            if e.args[0] not in [26, 13] and e.args[1] not in [
                "Text file busy",
                "Permission denied",
            ]:
                raise e
            file_names = []
            for n in archive.namelist():
                if "/" not in n:
                    file_names.append(n)
                else:
                    file_path, file_name = n.split("/")
                    full_file_path = os.path.join(to_directory, file_path)
                    source = os.path.join(full_file_path, file_name)
                    destination = os.path.join(to_directory, file_name)
                    os.rename(source, destination)
                    file_names.append(file_name)
            return sorted(file_names, key=lambda x: x.lower())
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

    def __extract_deb_file(self, to_directory):
        # NOTE: based on code from: https://github.com/memory/python-dpkg/blob/master/pydpkg/dpkg.py

        data_archive_type = None
        dpkg_archive = arpy.Archive(self.file_path)
        dpkg_archive.read_all_headers()
        if b"data.tar.gz" in dpkg_archive.archived_files:
            data_archive = dpkg_archive.archived_files[b"data.tar.gz"]
            data_archive_type = "gz"
        elif b"data.tar.xz" in dpkg_archive.archived_files:
            data_archive = dpkg_archive.archived_files[b"data.tar.xz"]
            data_archive_type = "xz"
        elif b"data.tar.zst" in dpkg_archive.archived_files:
            data_archive = dpkg_archive.archived_files[b"data.tar.zst"]
            data_archive_type = "zst"

        if data_archive_type == "gz":
            with GzipFile(fileobj=data_archive) as gzf:
                tar_archive = tarfile.open(fileobj=io.BytesIO(gzf.read()))
        elif data_archive_type == "xz":
            with lzma.open(data_archive) as xzf:
                tar_archive = tarfile.open(fileobj=io.BytesIO(xzf.read()))
        elif data_archive_type == "zst":
            zst = zstandard.ZstdDecompressor()
            with zst.stream_reader(data_archive) as reader:
                tar_archive = tarfile.open(fileobj=io.BytesIO(reader.read()))
        else:
            raise NotImplementedError('unsupported data archive type')

        members = []
        with tar_archive:
            members = tar_archive.getmembers()
            tar_archive.extractall(to_directory)

        return [x.name for x in members]