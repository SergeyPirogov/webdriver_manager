import tarfile
import zipfile


def extract_zip(zip_file, to_dir):
    """
    Method to extract the content of a zip
    :param zip_file: the zip file path
    :param to_dir: output directory
    :return: Return a list of file names in the archive.
    :rtype: list
    """
    archive = zipfile.ZipFile(zip_file)
    archive.extractall(to_dir)
    return archive.namelist()


def extract_tar_file(tar_file, to_dir):
    """
    Method to extract the content of a tar
    :param tar_file: the tar file path
    :param to_dir: output directory
    :return: Return a list of file names in the archive.
    :rtype: list
    """
    try:
        tar = tarfile.open(tar_file, mode="r:gz")
    except tarfile.ReadError:
        tar = tarfile.open(tar_file, mode="r:bz2")
    members = tar.getmembers()
    tar.extractall(to_dir)
    tar.close()
    return members
