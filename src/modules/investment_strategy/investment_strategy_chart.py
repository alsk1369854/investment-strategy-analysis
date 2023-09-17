from typing import List, Final, Set
from matplotlib import pyplot as plt
from pandas import Timestamp
from ...models.investment_strategy_model import InvestmentStrategy


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
            subplot: (plt.Figure, plt.Axes) = plt.subplots()
            figure: plt.Figure = subplot[0]
            axes: plt.Axes = subplot[1]

            for investment_strategy in self._investment_strategy_list:
                if timestamp_column_name != investment_strategy.timestamp_column_name:
                    break

                label_name: str = investment_strategy.name
                axis_x: List[Timestamp] = investment_strategy.timestamp_list
                axis_y: List[float] = investment_strategy.capital_list

                axes.plot(axis_x, axis_y, label=label_name)

            axes.xlabel("日期")
            axes.ylabel("資本")
            axes.title("資本線")
            axes.legend()
            plt.show()
            # axis_y =
