from typing import Any, Tuple, Dict
from customtkinter import (
    CTkTabview,
    CTkLabel,
    CTkFrame,
    CTkScrollbar,
    CTkScrollableFrame,
    END,
)

import pandas as pd
from tkinter import ttk
from enum import StrEnum
from .investment_strategy_info_frame import InvestmentStrategyInfoFrame
from ....utils import TkinterUtil
from ....modules import (
    thread_local_manager,
    InvestmentStrategy,
    InvestmentStrategyManager,
)


class TabEnum(StrEnum):
    table = "表格"
    investment_strategy_info = "策略訊息"
    investment_strategy_chart = "策略圖表"


class MainTabView(CTkTabview):
    def __init__(self, master: Any):
        super().__init__(master)

        # self.add("tab 1")

        # # add widgets on tabs
        # self.label = CTkLabel(master=self.tab("tab 1"))
        # self.label.grid(row=0, column=0, padx=20, pady=10)

        self._create_tabs()

    def refresh(self):
        self.refresh_tab_table()
        self.refresh_tab_strategy_info()

    def refresh_tab_strategy_info(self):
        tab_strategy_info_frame: CTkFrame = self.tab(TabEnum.investment_strategy_info)
        TkinterUtil.destroy_frame(
            tab_strategy_info_frame,
            after_destroy=self._build_tab_investment_strategy_info,
        )

    def refresh_tab_table(self):
        tab_table_frame: CTkFrame = self.tab(TabEnum.table)
        TkinterUtil.destroy_frame(
            tab_table_frame,
            after_destroy=self._build_tab_table,
        )

    def _create_tabs(self):
        self.add(TabEnum.table)
        self._build_tab_table()

        self.add(TabEnum.investment_strategy_info)
        self._build_tab_investment_strategy_info()

        self.add(TabEnum.investment_strategy_chart)
        self._build_tab_investment_strategy_chart()

    def _build_tab_investment_strategy_chart(self):
        # 數據準備
        investment_strategy_manager: InvestmentStrategyManager = (
            thread_local_manager.get_investment_strategy_manager()
        )
        # 獲取 tab_table_frame
        tab_investment_strategy_chart: CTkFrame = self.tab(
            TabEnum.investment_strategy_chart
        )
        strategy_chart_frame: CTkScrollableFrame = CTkScrollableFrame(
            tab_investment_strategy_chart
        )
        pass

    def _build_tab_investment_strategy_info(self):
        # 數據準備
        investment_strategy_manager: InvestmentStrategyManager = (
            thread_local_manager.get_investment_strategy_manager()
        )

        # 獲取 tab_table_frame
        tab_strategy_info_frame: CTkFrame = self.tab(TabEnum.investment_strategy_info)
        strategy_info_frame: CTkScrollableFrame = CTkScrollableFrame(
            tab_strategy_info_frame
        )
        # 投資策略訊息 Frame
        for investment_strategy in investment_strategy_manager.get_all():
            investment_strategy_info_frame: CTkFrame = InvestmentStrategyInfoFrame(
                strategy_info_frame, investment_strategy
            )
            investment_strategy_info_frame.pack(fill="x", pady=3)

        # layout
        strategy_info_frame.pack(expand=True, fill="both")

    def _build_tab_table(self):
        # 獲取 tab_table_frame
        tab_table_frame: CTkFrame = self.tab(TabEnum.table)

        # 讀取開啟的資料表
        base_data_frame: pd.DataFrame = thread_local_manager.get_base_data_frame()
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
