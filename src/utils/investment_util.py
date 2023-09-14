from typing import List
from enum import StrEnum
from pandas import Timestamp, DataFrame, period_range


class MaxDrawdownResult:
    def __init__(self, max_drawdown: float, start_date: Timestamp, end_date: Timestamp):
        self.max_drawdown: float = max_drawdown
        self.start_date: Timestamp = start_date
        self.end_date: Timestamp = end_date


class InvestmentUtil:
    @staticmethod
    # 計算年化收益率
    def annual_return(
        date_line: List[Timestamp],
        capital_line: List[float],
    ) -> float:
        """
        :param data_line: 日期序列
        :param capital_line: 帳戶價值序列
        :return: 輸出回測期間的年化收益率
        """

        # 將數據序列合併成 DataFrame 並按日期排序
        class Column(StrEnum):
            date = "date"
            capital = "capital"

        df: DataFrame = DataFrame(
            {
                Column.date: date_line,
                Column.capital: capital_line,
            }
        )
        df.sort_values(by=Column.date, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # 計算年化收益率
        start_capital: float = df.loc[0, Column.capital]
        end_capital: float = df.loc[len(df.index) - 1, Column.capital]
        total_return: float = end_capital / start_capital
        day_count: int = len(
            period_range(df[Column.date].iloc[0], df[Column.date].iloc[-1], freq="D")
        )
        year_count: float = day_count / 365
        annual: float = pow(total_return + 1, 1 / year_count) - 1
        return annual

    @staticmethod
    # 計算最大回測
    def max_drawdown(
        date_line: List[Timestamp], capital_line: List[float]
    ) -> MaxDrawdownResult:
        """
        :param data_line: 日期序列
        :param capital_line: 帳戶價值序列
        :return: 輸出 最大回測、開始日期、結束時間
        """

        # 將數據序列合併成 DataFrame 並按日期排序
        class Column(StrEnum):
            date = "date"
            capital = "capital"
            current_max = "current_max"  # 當日之前的張戶最大價值
            drawdown = "drawdown"  # 當日回撤

        df: DataFrame = DataFrame(
            {
                Column.date: date_line,
                Column.capital: capital_line,
            }
        )
        df.sort_values(by=Column.date, inplace=True)
        df.reset_index(drop=True, inplace=True)

        # 計算最大回撤和結束時間
        df[Column.current_max] = df[Column.capital].cummax()  # 計算當日之前的張戶最大價值
        df[Column.drawdown] = df[Column.capital] / df[Column.current_max] - 1  # 計算當日回撤

        temp: DataFrame = df.sort_values(by=Column.drawdown).iloc[0][
            [Column.date, Column.drawdown]
        ]
        max_drawdown: float = temp[Column.drawdown]
        end_date: Timestamp = temp[Column.date]

        # 計算開始時間
        df = df[df[Column.date] <= end_date]
        start_date: Timestamp = df.sort_values(by=Column.capital, ascending=False).iloc[
            0
        ][Column.date]

        return MaxDrawdownResult(max_drawdown, start_date, end_date)
