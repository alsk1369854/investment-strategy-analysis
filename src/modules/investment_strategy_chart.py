from typing import List, Final, Set
from matplotlib import pyplot as plt
from pandas import Timestamp
from .investment_strategy import InvestmentStrategy


class InvestmentStrategyChart:
    def __init__(self, investment_strategy_list: List[InvestmentStrategy]):
        self._investment_strategy_list: Final[
            List[InvestmentStrategy]
        ] = investment_strategy_list

    def capital_line_chart_list(self):
        timestamp_column_name_set: Set[str] = set()
        for investment_strategy in self._investment_strategy_list:
            timestamp_column_name_set.add(investment_strategy.timestamp_column_name)

        result_chart_list = []
        for timestamp_column_name in timestamp_column_name_set:
            for investment_strategy in self._investment_strategy_list:
                if timestamp_column_name != investment_strategy.timestamp_column_name:
                    break

                label_name: str = investment_strategy.name
                axis_x: List[Timestamp] = investment_strategy.timestamp_list
                axis_y: List[float] = investment_strategy.capital_list

                plt.plot(axis_x, axis_y, label=label_name)

            plt.xlabel("日期")
            plt.ylabel("資本")
            plt.title("資本線")
            plt.legend()
            plt.show()
            # axis_y =
