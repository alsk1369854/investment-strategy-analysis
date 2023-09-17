from typing import Any
from customtkinter import CTkLabel, CTkFrame, NW

from ....utils import RatioUtil
from ....modules.investment_strategy import InvestmentStrategy, MaxDrawdownResult
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
            self, text=f"起始日期: {data_start_datetime.date()}"
        )
        self._data_end_datetime_label: CTkLabel = CTkLabel(
            self, text=f"結束日期: {data_end_datetime.date()}"
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
            self, text=f"起始時間: {max_drawdown_start_timestamp.date()}"
        )
        self._max_drawdown_end_timestamp_label: CTkLabel = CTkLabel(
            self, text=f"結束時間: {max_drawdown_end_timestamp.date()}"
        )

    def _build_layout(self):
        # 策略名稱
        self._investment_strategy_name_label.grid(
            row=0, column=0, sticky=NW, padx=5, pady=2
        )

        # 資本列名
        self._capital_column_name_label.grid(row=1, column=0, sticky=NW, padx=5, pady=2)

        # 數據起始日期與結束日期
        self._data_start_datetime_label.grid(row=1, column=1, sticky=NW, padx=5, pady=2)
        self._data_end_datetime_label.grid(row=1, column=2, sticky=NW, padx=5, pady=2)

        # 年化收益率
        self._annual_return_ratio_label.grid(row=3, column=0, sticky=NW, padx=5, pady=2)

        # 夏普比率
        self._sharp_ratio_label.grid(row=4, column=0, sticky=NW, padx=5, pady=2)

        # 收益波動率
        self._earnings_volatility_ratio_label.grid(
            row=5, column=0, sticky=NW, padx=5, pady=2
        )

        # 最大回測
        self._max_drawdown_label.grid(row=6, column=0, sticky=NW, padx=5, pady=2)
        self._max_drawdown_start_timestamp_label.grid(
            row=6, column=1, sticky=NW, padx=5, pady=2
        )
        self._max_drawdown_end_timestamp_label.grid(
            row=6, column=2, sticky=NW, padx=5, pady=2
        )
