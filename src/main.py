from typing import List

import pandas as pd

# from pandas import DataFrame, read_excel, read_csv, to_datetime
from .modules import InvestmentStrategy, MaxDrawdownResult
from .gui import AppWindow


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


from .gui import AppWindow


class Main:
    def __init__(self):
        self.app_window: AppWindow = AppWindow(size=(900, 350))

    def start(self):
        self.app_window.mainloop()
