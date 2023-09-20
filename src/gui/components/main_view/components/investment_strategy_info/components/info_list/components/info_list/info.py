from typing import Any
from customtkinter import CTkFrame
from .components.title import Title
from .components.detail import Detail
from ..........models import InvestmentStrategyModel


class Info(CTkFrame):
    def __init__(
        self,
        master: Any,
        investment_strategy: InvestmentStrategyModel,
    ):
        super().__init__(master)
        self._investment_strategy: InvestmentStrategyModel = investment_strategy

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        self._title_frame: Title = Title(self, self._investment_strategy)
        self._detail_frame: Detail = Detail(self, self._investment_strategy)

    def _build_layout(self):
        self._title_frame.pack(fill="x", padx=5, pady=(5, 0))
        self._detail_frame.pack(fill="x", padx=5, pady=(0, 5))
