from typing import List

import pandas as pd

# from pandas import DataFrame, read_excel, read_csv, to_datetime
from .modules import InvestmentStrategyAnalysis, MaxDrawdownResult
from .gui import MainWindow


def get_data_frame(file_path: str) -> pd.DataFrame:
    file_extension: str = file_path.split(".")[-1]
    match file_extension:
        case "xlsx" | "xls":
            return pd.read_excel(file_path)
        case "csv":
            return pd.read_csv(file_path)
        case _:
            raise RuntimeError("file can not parse to data frame")


def init(data_frame: pd.DataFrame) -> pd.DataFrame:
    new_data_frame: pd.DataFrame = data_frame.copy(deep=True)

    # 格式化日期
    new_data_frame["Date"] = pd.to_datetime(new_data_frame["Date"], format="%m/%d/%Y")

    # # 日期排序
    # new_data_frame.sort_values(by="Date", inplace=True)

    # # 設定日期為 data_frame index
    # new_data_frame.set_index("Date", inplace=True)

    # 下架不需要的資料 columns
    new_data_frame.drop(
        columns=[
            "Price",
            "Open",
            "High",
            "Low",
            "Change %",
            "QLD",
            "季線上下",
            "季線上揚下彎",
            "兩種策略輸贏",
            "兩種策略差異幾%",
        ],
        inplace=True,
    )

    # 變更列名
    new_data_frame.rename(
        columns={
            "季線下彎AND\n收盤在季線下1倍\n其餘3倍": "策略一",
            "季線下彎AND\n收盤在季線下0倍\n其餘3倍": "策略二",
        },
        inplace=True,
    )

    # new_data_frame["new_column"] = new_data_frame["季線下彎AND\n收盤在季線下1倍\n其餘3倍"]

    return new_data_frame


from .gui import MainWindow
from customtkinter import CTk


class App:
    def __init__(self):
        pass

    def start(self):
        main_window: MainWindow = MainWindow()
        main_window.mainloop()
