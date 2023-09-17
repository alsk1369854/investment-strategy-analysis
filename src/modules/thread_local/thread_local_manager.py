# from typing import Dict
from threading import local
from pandas import DataFrame
from .investment_strategy_manager import InvestmentStrategyManager


class ThreadLocalManager(local):
    def __init__(self):
        super().__init__()
        self._base_data_frame: DataFrame = DataFrame()
        self._investment_strategy_manager: InvestmentStrategyManager = (
            InvestmentStrategyManager()
        )

    def get_base_data_frame(self) -> DataFrame:
        return self._base_data_frame

    def set_base_data_frame(self, value: DataFrame):
        self._base_data_frame = value

    def get_investment_strategy_manager(self) -> InvestmentStrategyManager:
        return self._investment_strategy_manager

    def clear_investment_strategy_manager(self):
        self._investment_strategy_manager.clear()


thread_local_manager: ThreadLocalManager = ThreadLocalManager()
