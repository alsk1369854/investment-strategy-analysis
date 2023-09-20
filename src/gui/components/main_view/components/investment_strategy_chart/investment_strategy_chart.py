from typing import Any
from customtkinter import CTkScrollableFrame
from .components.annual_return_ratio_chart import AnnualReturnRatioChart


class InvestmentStrategyChart(CTkScrollableFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        self._annual_return_ratio_chart: AnnualReturnRatioChart = (
            AnnualReturnRatioChart(self)
        )

    def _build_layout(self):
        self._annual_return_ratio_chart.pack(fill="x", expand=True)
