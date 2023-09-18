from typing import Self
from .investment_strategy_service import InvestmentStrategyService
from .base_data_frame_service import BaseDataFrameService
from .max_drawdown_service import MaxDrawdownService
from ..libs.bean_factory import bean


@bean
class Services:
    instance: Self
    investment_strategy_service: InvestmentStrategyService
    base_data_frame_service: BaseDataFrameService
    max_drawdown_service: MaxDrawdownService

    def __init__(self):
        self.__class__.instance = self
