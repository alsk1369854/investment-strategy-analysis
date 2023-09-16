from typing import Dict
from threading import local
from pandas import DataFrame
from ..modules import InvestmentStrategy

_thread_local: local = local()
_thread_local.base_data_frame: DataFrame = DataFrame()
_thread_local.investment_strategy_dict: Dict[str, InvestmentStrategy] = {}


class ThreaLocalUtil:
    @staticmethod
    def get_base_data_frame() -> DataFrame:
        return _thread_local.base_data_frame

    @staticmethod
    def set_base_data_frame(value: DataFrame):
        _thread_local.base_data_frame = value

    @staticmethod
    def get_investment_strategy_dict() -> Dict[str, InvestmentStrategy]:
        return _thread_local.investment_strategy_dict

    @staticmethod
    def set_investment_strategy_dict(value: Dict[str, InvestmentStrategy]):
        _thread_local.investment_strategy_dict = value
