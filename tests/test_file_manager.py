import zipfile

from webdriver_manager.core.file_manager import FileManager
from webdriver_manager.core.os_manager import OperationSystemManager


def test_extract_zip_removes_file_dir_conflict(tmp_path):
    target_dir = tmp_path / "target"
    target_dir.mkdir()
    conflict_path = target_dir / "operadriver"
    conflict_path.write_text("stale file")

    zip_path = tmp_path / "driver.zip"
    with zipfile.ZipFile(zip_path, "w") as zf:
        zf.writestr("operadriver/operadriver", "binary")

    class ArchiveMock:
        def __init__(self, file_path):
            self.file_path = str(file_path)

    file_manager = FileManager(OperationSystemManager())
    extracted = file_manager.unpack_archive(ArchiveMock(zip_path), str(target_dir))

    assert "operadriver/operadriver" in extracted
    assert (target_dir / "operadriver" / "operadriver").exists()
