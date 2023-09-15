from typing import Final, List
from .system_util import SystemUtil


class FileUtil:
    excel_extension: Final[List[str]] = ["xlsx", "xls"]
    csv_extension: Final[List[str]] = ["csv"]

    @staticmethod
    def get_file_name(file_path: str) -> str:
        if file_path == "":
            raise RuntimeError("file_path is empty")

        file_path_split: List[str] = []
        if SystemUtil.is_windows():
            file_path_split = file_path.split("\\")
        elif SystemUtil.is_linux() | SystemUtil.is_macOS():
            file_path_split = file_path.split("/")

        file_name: str = file_path_split[-1]
        return file_name

    @staticmethod
    def get_file_extension(file_path: str) -> str:
        file_name: str = FileUtil.get_file_name(file_path)

        file_name_split: List[str] = file_name.split(".")
        if len(file_name_split) < 2:
            return ""

        file_extension: str = file_name_split[-1]
        return file_extension

    @staticmethod
    def is_excel_file(file_path: str) -> bool:
        file_extension: str = FileUtil.get_file_extension(file_path)
        for excel_extension in FileUtil.excel_extension:
            if file_extension == excel_extension:
                return True

        return False

    @staticmethod
    def is_csv_file(file_path: str) -> bool:
        file_extension: str = FileUtil.get_file_extension(file_path)
        for csv_extension in FileUtil.csv_extension:
            if file_extension == csv_extension:
                return True

        return False
