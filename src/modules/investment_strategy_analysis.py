from typing import List, Final
from enum import StrEnum, Enum
from pandas import Timestamp, DataFrame, period_range
from math import sqrt


class ColumnEnum(StrEnum):
    timestamp = "timestamp"
    capital = "capital"
    day_earnings = "day_earnings"


class MaxDrawdownResult:
    def __init__(self, max_drawdown: float, start_date: Timestamp, end_date: Timestamp):
        self.max_drawdown: Final[float] = max_drawdown
        self.start_date: Final[Timestamp] = start_date
        self.end_date: Final[Timestamp] = end_date


class InvestmentStrategyAnalysis:
    def __init__(self, timestamp_line: List[Timestamp], capital_line: List[float]):
        """
        :param timestamp_line: 日期時間序列資料
        :param capital_line: 帳戶資本序列資料
        """
        # 建立 DataFrame
        self._df: DataFrame = DataFrame(
            {
                ColumnEnum.timestamp: timestamp_line,
                ColumnEnum.capital: capital_line,
            }
        )
        self._df.sort_values(by=ColumnEnum.timestamp, inplace=True)
        self._df.reset_index(drop=True, inplace=True)

        # 建立日收益率 Column
        day_earnings_line: List[float] = []
        capital_line_sorted: List[float] = list(self._df[ColumnEnum.capital])
        capital_line_sorted_len: int = len(capital_line_sorted)
        if capital_line_sorted_len >= 1:
            day_earnings_line.append(0)
            for i in range(1, len(capital_line_sorted)):
                yesterday_capital: float = capital_line_sorted[i - 1]
                today_capital: float = capital_line_sorted[i]

                # 日收益率 = (今日資本 - 昨日資本) / 昨日資本
                day_earnings: float = (
                    today_capital - yesterday_capital
                ) / yesterday_capital

                day_earnings_line.append(day_earnings)
        self._df[ColumnEnum.day_earnings] = day_earnings_line

    # 計算年化收益率
    def annual_return_ratio(self) -> float:
        start_capital: float = self._df.loc[0, ColumnEnum.capital]
        end_capital: float = self._df.loc[len(self._df.index) - 1, ColumnEnum.capital]
        total_return: float = end_capital / start_capital
        day_count: int = len(
            period_range(
                self._df[ColumnEnum.timestamp].iloc[0],
                self._df[ColumnEnum.timestamp].iloc[-1],
                freq="D",
            )
        )
        year_count: float = day_count / 365
        annual: float = pow(total_return + 1, 1 / year_count) - 1
        return annual

    # 計算最大回測
    def max_drawdown(self) -> MaxDrawdownResult:
        # 將數據序列合併成 DataFrame 並按日期排序
        class LocalColumnEnum(StrEnum):
            timestamp = ColumnEnum.timestamp
            capital = ColumnEnum.capital
            current_max = "current_max"  # 當日之前的張戶最大價值
            drawdown = "drawdown"  # 當日回撤

        local_df: DataFrame = DataFrame(
            {
                LocalColumnEnum.timestamp: self._df[ColumnEnum.timestamp],
                LocalColumnEnum.capital: self._df[ColumnEnum.capital],
            }
        )
        local_df[LocalColumnEnum.current_max] = local_df[
            LocalColumnEnum.capital
        ].cummax()  # 計算當日之前的張戶最大價值
        local_df[LocalColumnEnum.drawdown] = (
            local_df[LocalColumnEnum.capital] / local_df[LocalColumnEnum.current_max]
            - 1
        )  # 計算當日回撤

        # 計算最大回撤和結束時間
        temp: DataFrame = local_df.sort_values(by=LocalColumnEnum.drawdown).iloc[0][
            [LocalColumnEnum.timestamp, LocalColumnEnum.drawdown]
        ]
        max_drawdown: float = temp[LocalColumnEnum.drawdown]
        end_date: Timestamp = temp[LocalColumnEnum.timestamp]

        # 計算開始時間
        local_df = local_df[local_df[LocalColumnEnum.timestamp] <= end_date]
        start_date: Timestamp = local_df.sort_values(
            by=LocalColumnEnum.capital, ascending=False
        ).iloc[0][LocalColumnEnum.timestamp]

        return MaxDrawdownResult(max_drawdown, start_date, end_date)

    # 計算收益波動率
    def earnings_volatility_ratio(self) -> float:
        return self._df[ColumnEnum.day_earnings].std() % sqrt(250)

    # 夏普比率
    def sharp_ratio(self) -> float:
        annual_return_ratio: float = self.annual_return_ratio()
        earnings_volatility_ratio: float = self.earnings_volatility_ratio()
        rf: float = 0.0284  # 無風險利率取 10 年期國債的到期年化收益率
        sharp_ratio: float = (annual_return_ratio - rf) / earnings_volatility_ratio
        return sharp_ratio
