from customtkinter import (
    CTkFrame,
    CTkLabel,
    StringVar,
    CTkComboBox,
    CTkButton,
    NSEW,
    NW,
)
from typing import Any


class InvestmentStrategyFormFrame(CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        # title
        self._frame_title: CTkLabel = CTkLabel(self, text="策略分析配置表")

        # timestamp column selector
        self._timestamp_column_name_label: CTkLabel = CTkLabel(self, text="日期列:")
        self._timestamp_column_name: StringVar = StringVar(value="option 1")
        self._timestamp_column_name_selector: CTkComboBox = CTkComboBox(
            self,
            values=["option 1", "option 2"],
            variable=self._timestamp_column_name,
        )

        # capital column selector
        self._capital_column_name_label: CTkLabel = CTkLabel(self, text="資產列:")
        self._capital_column_name: StringVar = StringVar(value="option 1")
        self._capital_column_name_selector: CTkComboBox = CTkComboBox(
            self,
            values=["option 1", "option 2"],
            variable=self._timestamp_column_name,
        )

        # create btn
        self._create_btn: CTkButton = CTkButton(self, text="創建")

    def _build_layout(self):
        # title
        self._frame_title.grid(row=0, column=0, columnspan=2, sticky=NSEW)

        # timestamp column selector
        self._timestamp_column_name_label.grid(
            row=1, column=0, padx=5, pady=5, sticky=NW
        )
        self._timestamp_column_name_selector.grid(
            row=1, column=1, padx=5, pady=5, sticky=NW
        )

        # capital column selector
        self._capital_column_name_label.grid(row=2, column=0, padx=5, pady=5, sticky=NW)
        self._capital_column_name_selector.grid(
            row=2, column=1, padx=5, pady=5, sticky=NW
        )

        # create btn
        self._create_btn.grid(
            row=3, column=0, columnspan=2, padx=5, pady=5, sticky=NSEW
        )
