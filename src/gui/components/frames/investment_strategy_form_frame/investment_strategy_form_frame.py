from typing import Any, List, Dict, Callable, Optional
from customtkinter import (
    CTkFrame,
    CTkLabel,
    StringVar,
    CTkComboBox,
    CTkButton,
    CTkEntry,
    NSEW,
    NW,
)
from ...modules.thread_local import thread_local_manager
from ...modules.investment_strategy import InvestmentStrategy, InvestmentStrategyManager
from .date_picker_top_window import DatePickerTopWindow, DATE_PICKER_FORMAT_CODE
from ...utils import TkinterUtil
from datetime import datetime
import pandas as pd


DEFAULT_DATE_PICKER_SELECTED_VALUE = "點擊選擇日期"
BASICE_INVESTMENT_STRATEGY_NAME = "投資策略"


class InvestmentStrategyFormFrame(CTkFrame):
    def __init__(
        self,
        master: Any,
        on_submit: Optional[Callable[[InvestmentStrategy], None]] = None,
    ):
        super().__init__(master)
        self.on_submit: Optional[Callable[[InvestmentStrategy], None]] = on_submit

        self._create_widgets()
        self._build_layout()

    def refresh(self):
        def after_self_widgets_destroy():
            self._create_widgets()
            self._build_layout()

        TkinterUtil.destroy_frame(self, after_destroy=after_self_widgets_destroy)

    def _create_widgets(self):
        # 數據載入
        # base_data_frame
        base_data_frame: pd.DataFrame = thread_local_manager.get_base_data_frame()
        base_data_frame_column_name_lise: List[str] = list(base_data_frame.columns)
        base_data_frame_column_name_lise_len: int = len(
            base_data_frame_column_name_lise
        )
        # 標頭
        self._frame_title: CTkLabel = CTkLabel(self, text="策略分析配置表")

        # 策略名稱 輸入
        self._investment_strategy_name: StringVar = StringVar(
            value=f"{BASICE_INVESTMENT_STRATEGY_NAME}_{InvestmentStrategy.get_instance_count() + 1}"
        )
        self._investment_strategy_name_label: CTkLabel = CTkLabel(self, text="策略名稱:")
        self._investment_strategy_name_input: CTkEntry = CTkEntry(
            self,
            placeholder_text=BASICE_INVESTMENT_STRATEGY_NAME,
            textvariable=self._investment_strategy_name,
        )

        # 日期格式 輸入
        self._timestamp_format_code: StringVar = StringVar(value="%m/%d/%Y")
        self._timestamp_format_code_label: CTkLabel = CTkLabel(self, text="日期格式:")
        self._timestamp_format_code_input: CTkEntry = CTkEntry(
            self, placeholder_text="日期格式", textvariable=self._timestamp_format_code
        )

        # 日期列 選擇器
        self._timestamp_column_name: StringVar = StringVar()
        self._timestamp_column_name_label: CTkLabel = CTkLabel(self, text="日期列:")
        self._timestamp_column_name_selector: CTkComboBox = CTkComboBox(
            self,
            values=base_data_frame_column_name_lise,
            variable=self._timestamp_column_name,
        )
        if base_data_frame_column_name_lise_len > 0:
            self._timestamp_column_name.set(base_data_frame_column_name_lise[0])

        # 資本列 選擇器
        self._capital_column_name: StringVar = StringVar()
        self._capital_column_name_label: CTkLabel = CTkLabel(self, text="資本列:")
        self._capital_column_name_selector: CTkComboBox = CTkComboBox(
            self,
            values=base_data_frame_column_name_lise,
            variable=self._capital_column_name,
        )
        if base_data_frame_column_name_lise_len > 0:
            self._capital_column_name.set(base_data_frame_column_name_lise[0])

        # 起始時間 日期選擇器
        self._start_date_label: CTkLabel = CTkLabel(self, text="起始時間:")
        self._start_date: StringVar = StringVar(
            value=DEFAULT_DATE_PICKER_SELECTED_VALUE
        )
        self._start_date_show_label: CTkLabel = CTkLabel(
            self,
            text=self._start_date.get(),
        )
        self._start_date_show_label.bind(
            "<Button-1>", self._start_date_show_label_click_handler
        )
        self._start_date_pikcer: DatePickerTopWindow = None

        # 結束時間 日期選擇器
        self._end_date_label: CTkLabel = CTkLabel(self, text="結束時間:")
        self._end_date: StringVar = StringVar(value=DEFAULT_DATE_PICKER_SELECTED_VALUE)
        self._end_date_show_label: CTkLabel = CTkLabel(
            self,
            text=self._end_date.get(),
        )
        self._end_date_show_label.bind(
            "<Button-1>", self._end_date_show_label_click_handler
        )
        self._end_date_pikcer: DatePickerTopWindow = None

        # 創建 按鈕
        self._create_btn: CTkButton = CTkButton(
            self, text="創建", command=self._create_btn_click_handler
        )

    def _build_layout(self):
        # 標頭
        self._frame_title.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # 策略名稱 輸入
        self._investment_strategy_name_label.grid(
            row=1, column=0, padx=5, pady=5, sticky=NW
        )
        self._investment_strategy_name_input.grid(
            row=1, column=1, padx=5, pady=5, sticky=NW
        )

        # 日期格式 輸入
        self._timestamp_format_code_label.grid(
            row=2, column=0, padx=5, pady=5, sticky=NW
        )
        self._timestamp_format_code_input.grid(
            row=2, column=1, padx=5, pady=5, sticky=NW
        )

        # 日期列 選擇器
        self._timestamp_column_name_label.grid(
            row=3, column=0, padx=5, pady=5, sticky=NW
        )
        self._timestamp_column_name_selector.grid(
            row=3, column=1, padx=5, pady=5, sticky=NW
        )

        # 資本列 選擇器
        self._capital_column_name_label.grid(row=4, column=0, padx=5, pady=5, sticky=NW)
        self._capital_column_name_selector.grid(
            row=4, column=1, padx=5, pady=5, sticky=NW
        )

        # 起始時間 日期選擇器
        self._start_date_label.grid(row=5, column=0, padx=5, pady=5, sticky=NW)
        self._start_date_show_label.grid(row=5, column=1, padx=5, pady=5, sticky=NSEW)

        # 結束時間 日期選擇器
        self._end_date_label.grid(row=6, column=0, padx=5, pady=5, sticky=NW)
        self._end_date_show_label.grid(row=6, column=1, padx=5, pady=5, sticky=NSEW)

        # 創建 按鈕
        self._create_btn.grid(
            row=7, column=0, columnspan=2, padx=5, pady=5, sticky=NSEW
        )

    def _create_btn_click_handler(self):
        # 數據載入
        # base_data_frame
        base_data_frame: pd.DataFrame = thread_local_manager.get_base_data_frame()
        # investement_strategy_manager
        investment_strategy_manager: InvestmentStrategyManager = (
            thread_local_manager.get_investment_strategy_manager()
        )

        # 創建分析數據
        investment_strategy_name: str = self._investment_strategy_name.get()
        timestamp_column_name: str = self._timestamp_column_name.get()
        timestamp_format_code: str = self._timestamp_format_code.get()
        capital_column_name: str = self._capital_column_name.get()
        data_start_datetime: datetime = datetime.strptime(
            self._start_date.get(), DATE_PICKER_FORMAT_CODE
        )
        data_end_datetime: datetime = datetime.strptime(
            self._end_date.get(), DATE_PICKER_FORMAT_CODE
        )

        # 建立並註冊至 investment_strategy_dict
        investment_strategy: InvestmentStrategy = InvestmentStrategy(
            name=investment_strategy_name,
            base_data_frame=base_data_frame,
            timestamp_column_name=timestamp_column_name,
            timestamp_format_code=timestamp_format_code,
            capital_column_name=capital_column_name,
            data_start_datetime=data_start_datetime,
            data_end_datetime=data_end_datetime,
        )
        investment_strategy_manager.add(investment_strategy)

        # 更新 GUI
        self._investment_strategy_name.set(
            f"{BASICE_INVESTMENT_STRATEGY_NAME}_{InvestmentStrategy.get_instance_count() + 1}"
        )

        if self.on_submit != None:
            self.on_submit(investment_strategy)

    def _start_date_show_label_click_handler(self, event):
        def selected_handler(selected_date: str):
            self._start_date_show_label.configure(text=selected_date)
            self._start_date.set(selected_date)

        if (
            self._start_date_pikcer is None
            or not self._start_date_pikcer.winfo_exists()
        ):
            self._start_date_pikcer = DatePickerTopWindow(
                self, selected_handler=selected_handler, title="起始日期選擇器"
            )
        else:
            self._start_date_pikcer.focus()

    def _end_date_show_label_click_handler(self, event):
        def selected_handler(selected_date: str):
            self._end_date_show_label.configure(text=selected_date)
            self._end_date.set(selected_date)

        if self._end_date_pikcer is None or not self._end_date_pikcer.winfo_exists():
            self._end_date_pikcer = DatePickerTopWindow(
                self, selected_handler=selected_handler, title="結束日期選擇器"
            )
        else:
            self._end_date_pikcer.focus()
