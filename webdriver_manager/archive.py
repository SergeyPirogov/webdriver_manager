import tarfile
import zipfile


class Archive(object):

    def __init__(self, path: str):
        self.file_path = path

    def unpack(self, directory):
        if self.file_path.endswith(".zip"):
            return self.__extract_zip(directory)

    def __extract_zip(self, to_directory):
        archive = zipfile.ZipFile(self.file_path)
        archive.extractall(to_directory)
        return archive.namelist()


def extract_zip(zip_file, to_directory):
    archive = zipfile.ZipFile(zip_file)
    archive.extractall(to_directory)
    return archive.namelist()


def extract_tar_file(tar_file_path, to_dir):
    try:
        tar = tarfile.open(tar_file_path, mode="r:gz")
    except tarfile.ReadError:
        tar = tarfile.open(tar_file_path, mode="r:bz2")
    members = tar.getmembers()
    tar.extractall(to_dir)
    tar.close()
    return members
