from typing import Dict, List
from .investment_strategy_model import InvestmentStrategy


class InvestmentStrategyManager:
    def __init__(self):
        self._investment_strategy_dict: Dict[int, InvestmentStrategy] = {}

    def add(self, investment_strategy: InvestmentStrategy):
        instance_numbe: int = investment_strategy._instance_number
        self._investment_strategy_dict[instance_numbe] = investment_strategy

    def delete(self, investment_strategy: InvestmentStrategy):
        instance_numbe: int = investment_strategy._instance_number
        del self._investment_strategy_dict[instance_numbe]

    def get_all(self) -> List[InvestmentStrategy]:
        return list(self._investment_strategy_dict.values())

    def clear(self):
        self._investment_strategy_dict.clear()
