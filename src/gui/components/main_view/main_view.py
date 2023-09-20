from typing import Any, Tuple, List
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
from .components.investment_strategy_info import InvestmentStrategyInfo
from ....libs.pubsub import PubSub
from ..file_select_bar import PUBSUB_KEY_FILE_SELECTED
from ..create_investment_strategy_form import (
    PUBSUB_KEY_CREATE_INVESTMENT_STRATEGY_FORM_SUBMIT,
)
from ....utils import TkinterUtil
from ....models import InvestmentStrategyModel
from ....services import services_instance


class TabEnum(StrEnum):
    table = "表格"
    investment_strategy_info = "策略訊息"
    investment_strategy_chart = "策略圖表"


class MainView(CTkTabview):
    def __init__(self, master: Any):
        super().__init__(master)

        # self.add("tab 1")

        # # add widgets on tabs
        # self.label = CTkLabel(master=self.tab("tab 1"))
        # self.label.grid(row=0, column=0, padx=20, pady=10)

        self._create_tabs()

        PubSub.subscribe(PUBSUB_KEY_FILE_SELECTED, self._on_file_selected)
        PubSub.subscribe(
            PUBSUB_KEY_CREATE_INVESTMENT_STRATEGY_FORM_SUBMIT,
            self._on_create_investment_strategy_form_submit,
        )

    def destroy(self):
        PubSub.unsubscribe(PUBSUB_KEY_FILE_SELECTED, self._on_file_selected)
        PubSub.unsubscribe(
            PUBSUB_KEY_CREATE_INVESTMENT_STRATEGY_FORM_SUBMIT,
            self._on_create_investment_strategy_form_submit,
        )

        return super().destroy()

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

        # 獲取 tab_table_frame
        tab_investment_strategy_chart: CTkFrame = self.tab(
            TabEnum.investment_strategy_chart
        )
        strategy_chart_frame: CTkScrollableFrame = CTkScrollableFrame(
            tab_investment_strategy_chart
        )
        pass

    def _build_tab_investment_strategy_info(self):
        # 獲取 tab_table_frame
        tab_strategy_info_frame: CTkFrame = self.tab(TabEnum.investment_strategy_info)

        # 建立 投資策略 frame
        investment_info_frame: InvestmentStrategyInfo = InvestmentStrategyInfo(
            tab_strategy_info_frame
        )
        investment_info_frame.pack(expand=True, fill="both")

    def _build_tab_table(self):
        # 獲取 tab_table_frame
        tab_table_frame: CTkFrame = self.tab(TabEnum.table)

        # 讀取開啟的資料表
        base_data_frame: pd.DataFrame = (
            services_instance.base_data_frame_service.get_data_frame()
        )
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

    # pubsub handler
    def _on_file_selected(self, name: str, file_path: str):
        self.refresh()

    # pubsub handler
    def _on_create_investment_strategy_form_submit(
        self, name: str, investment_strategy: InvestmentStrategyModel
    ):
        self.refresh_tab_strategy_info()
