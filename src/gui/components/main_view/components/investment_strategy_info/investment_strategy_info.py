from typing import Any
from customtkinter import CTkFrame
from .components.info_list import InfoList
from .components.header_bar import HeaderBar


class InvestmentStrategyInfo(CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        self._header_bar_frame: HeaderBar = HeaderBar(self)
        self._info_list_frame: InfoList = InfoList(self)

    def _build_layout(self):
        self._header_bar_frame.pack(fill="x", padx=5, pady=(5, 0))
        self._info_list_frame.pack(expand=True, fill="both", padx=5, pady=5)
