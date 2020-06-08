import tarfile
import zipfile


class Archive(object):

    def __init__(self, path: str):
        self.file_path = path

    def unpack(self, directory):
        if self.file_path.endswith(".zip"):
            return self.__extract_zip(directory)
        elif self.file_path.endswith(".tar.gz"):
            return self.__extract_tar_file(directory)

    def __extract_zip(self, to_directory):
        archive = zipfile.ZipFile(self.file_path)
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
