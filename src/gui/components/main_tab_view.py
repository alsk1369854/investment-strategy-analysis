from typing import Any, Tuple, Dict
from customtkinter import (
    CTkTabview,
    CTkLabel,
    CTkFrame,
    CTkScrollbar,
    CTkScrollableFrame,
    END,
    NW,
)

from tkinter import ttk
from enum import StrEnum
from ...utils import ThreaLocalUtil, RatioUtil
from ...modules import InvestmentStrategy, MaxDrawdownResult
import pandas as pd
from datetime import datetime


class InvestmentStrategyInfoFrame(CTkFrame):
    def __init__(
        self,
        master: Any,
        investment_strategy: InvestmentStrategy,
    ):
        super().__init__(master)
        self.investment_strategy: InvestmentStrategy = investment_strategy

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        # 策略名稱
        investment_strategy_name: str = self.investment_strategy.name
        self._investment_strategy_name_label: CTkLabel = CTkLabel(
            self, text=f"策略名稱: {investment_strategy_name}"
        )

        # 策略資訊
        # 資本列名
        capital_column_name: str = self.investment_strategy.capital_column_name
        self._capital_column_name_label: CTkLabel = CTkLabel(
            self, text=f"資本列: {capital_column_name}"
        )
        # 數據起始日期與結束日期
        data_start_datetime: datetime = self.investment_strategy.data_start_datetime
        data_end_datetime: datetime = self.investment_strategy.data_end_datetime
        self._data_start_datetime_label: CTkLabel = CTkLabel(
            self, text=f"起始日期: {data_start_datetime}"
        )
        self._data_end_datetime_label: CTkLabel = CTkLabel(
            self, text=f"結束日期: {data_end_datetime}"
        )

        # 年化收益率
        annual_return_ratio: float = self.investment_strategy.annual_return_ratio()
        self._annual_return_ratio_label: CTkLabel = CTkLabel(
            self, text=f"年化收益率: {RatioUtil.parse_to_percent_str(annual_return_ratio)}"
        )

        # 夏普比率
        sharp_ratio: float = self.investment_strategy.sharp_ratio()
        self._sharp_ratio_label: CTkLabel = CTkLabel(
            self, text=f"夏普比率: {RatioUtil.parse_to_percent_str(sharp_ratio)}"
        )

        # 收益波動率
        earnings_volatility_ratio: float = (
            self.investment_strategy.earnings_volatility_ratio()
        )
        self._earnings_volatility_ratio_label: CTkLabel = CTkLabel(
            self,
            text=f"收益波動率: {RatioUtil.parse_to_percent_str(earnings_volatility_ratio)}",
        )

        # 最大回測
        max_drawdown_result: MaxDrawdownResult = self.investment_strategy.max_drawdown()
        max_drawdown: float = max_drawdown_result.max_drawdown
        max_drawdown_start_timestamp: pd.Timestamp = max_drawdown_result.start_timestamp
        max_drawdown_end_timestamp: pd.Timestamp = max_drawdown_result.end_timestamp
        self._max_drawdown_label: CTkLabel = CTkLabel(
            self, text=f"最大回測: {RatioUtil.parse_to_percent_str(max_drawdown)}"
        )
        self._max_drawdown_start_timestamp_label: CTkLabel = CTkLabel(
            self, text=f"起始時間: {max_drawdown_start_timestamp}"
        )
        self._max_drawdown_end_timestamp_label: CTkLabel = CTkLabel(
            self, text=f"結束時間: {max_drawdown_end_timestamp}"
        )

    def _build_layout(self):
        # 策略名稱
        self._investment_strategy_name_label.grid(
            row=0, column=0, sticky=NW, padx=2, pady=2
        )

        # 資本列名
        self._capital_column_name_label.grid(row=1, column=0, sticky=NW, padx=2, pady=2)

        # 數據起始日期與結束日期
        self._data_start_datetime_label.grid(row=1, column=1, sticky=NW, padx=2, pady=2)
        self._data_end_datetime_label.grid(row=1, column=2, sticky=NW, padx=2, pady=2)

        # 年化收益率
        self._annual_return_ratio_label.grid(row=3, column=0, sticky=NW, padx=2, pady=2)

        # 夏普比率
        self._sharp_ratio_label.grid(row=4, column=0, sticky=NW, padx=2, pady=2)

        # 收益波動率
        self._earnings_volatility_ratio_label.grid(
            row=5, column=0, sticky=NW, padx=2, pady=2
        )

        # 最大回測
        self._max_drawdown_label.grid(row=6, column=0, sticky=NW, padx=2, pady=2)
        self._max_drawdown_start_timestamp_label.grid(
            row=6, column=1, sticky=NW, padx=2, pady=2
        )
        self._max_drawdown_end_timestamp_label.grid(
            row=6, column=2, sticky=NW, padx=2, pady=2
        )


class TabEnum(StrEnum):
    table = "表格"
    investment_strategy_info = "策略訊息"
    # strategy_capital_chart = "策略圖表"


class MainTabView(CTkTabview):
    def __init__(self, master: Any):
        super().__init__(master)

        # self.add("tab 1")

        # # add widgets on tabs
        # self.label = CTkLabel(master=self.tab("tab 1"))
        # self.label.grid(row=0, column=0, padx=20, pady=10)

        self._create_tabs()

    def refresh(self):
        self._delete_tabs()
        self._create_tabs()

    def refresh_tab_strategy_info(self):
        self.delete(TabEnum.investment_strategy_info)
        self._create_tab_investment_strategy_info()

    def _create_tabs(self):
        self._create_tab_table()
        self._create_tab_investment_strategy_info()

    def _delete_tabs(self):
        for tab_enum_data in TabEnum:
            self.delete(tab_enum_data.value)

    def _create_tab_investment_strategy_info(self):
        # 數據準備
        investment_strategy_dict: Dict[
            str, InvestmentStrategy
        ] = ThreaLocalUtil.get_investment_strategy_dict()

        # 創建 tab_table_frame
        self.add(TabEnum.investment_strategy_info)
        tab_strategy_info_frame: CTkFrame = self.tab(TabEnum.investment_strategy_info)
        strategy_info_frame: CTkScrollableFrame = CTkScrollableFrame(
            tab_strategy_info_frame
        )
        # 投資策略訊息 Frame
        for key in investment_strategy_dict:
            investment_strategy: InvestmentStrategy = investment_strategy_dict[key]
            investment_strategy_info_frame: CTkFrame = InvestmentStrategyInfoFrame(
                strategy_info_frame, investment_strategy
            )
            investment_strategy_info_frame.pack(fill="x", pady=3)

        # layout
        strategy_info_frame.pack(expand=True, fill="both")

    def _create_tab_table(self):
        # 創建 tab_table_frame
        self.add(TabEnum.table)
        tab_table_frame: CTkFrame = self.tab(TabEnum.table)

        # 讀取開啟的資料表
        base_data_frame: pd.DataFrame = ThreaLocalUtil.get_base_data_frame()
        column_name_tuple: Tuple[str] = tuple(
            column for column in base_data_frame.columns
        )

        # 表格 滾動條
        table_scroll_bar: CTkScrollbar = CTkScrollbar(tab_table_frame)

        # 表格
        table: ttk.Treeview = ttk.Treeview(
            tab_table_frame,
            show="headings",
            columns=column_name_tuple,
            yscrollcommand=table_scroll_bar.set,
            height=13,
        )
        # 幫定滾動條事件
        table_scroll_bar.configure(command=table.yview)

        # 設定 column 名與寬
        for i, column_name in enumerate(column_name_tuple):
            table.column(i, width=len(column_name))
            table.heading(i, text=column_name)

        # 設定 row 數據
        for row_tuples in base_data_frame.itertuples(index=False):
            table.insert("", END, values=row_tuples)

        # layout
        table_scroll_bar.pack(side="right", fill="y")
        table.pack(expand=True, fill="both")
