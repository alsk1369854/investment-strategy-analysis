# from typing import
from pandas import read_excel, read_csv, DataFrame
from .file_util import FileUtil


class PandasUtil:
    @staticmethod
    def read_file(file_path: str) -> DataFrame:
        if FileUtil.is_excel_file(file_path):
            return read_excel(file_path)
        elif FileUtil.is_csv_file(file_path):
            return read_csv(file_path)
        else:
            raise RuntimeError("file can not parse to data frame")
