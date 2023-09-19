from typing import List, Final
from enum import StrEnum
from pandas import Timestamp, DataFrame, period_range, Series, to_datetime
from math import sqrt
from datetime import datetime


class ColumnEnum(StrEnum):
    timestamp = "timestamp"
    capital = "capital"
    day_earnings = "day_earnings"


class MaxDrawdownResult:
    def __init__(
        self, max_drawdown: float, start_timestamp: Timestamp, end_timestamp: Timestamp
    ):
        self.max_drawdown: Final[float] = max_drawdown
        self.start_timestamp: Final[Timestamp] = start_timestamp
        self.end_timestamp: Final[Timestamp] = end_timestamp


class InvestmentStrategyModel:
    _instance_count: int = 0

    @staticmethod
    def get_instance_count() -> int:
        return InvestmentStrategyModels._instance_count

    @staticmethod
    def next_instance_number() -> int:
        InvestmentStrategyModels._instance_count += 1
        return InvestmentStrategyModels._instance_count

    def __init__(
        self,
        name: str,
        base_data_frame: DataFrame,
        timestamp_column_name: str,  # 日期時間序列資料
        timestamp_format_code: str,
        capital_column_name: str,  # 帳戶資本序列資料
        data_start_datetime: datetime,
        data_end_datetime: datetime,
    ):
        self._instance_number: int = InvestmentStrategy.next_instance_number()
        self.name: str = name
        self.base_data_frame: DataFrame = base_data_frame
        self.timestamp_column_name: str = timestamp_column_name  # 日期時間序列資料
        self.timestamp_format_code: str = timestamp_format_code
        self.capital_column_name: str = capital_column_name  # 帳戶資本序列資料
        self.data_start_datetime: datetime = data_start_datetime
        self.data_end_datetime: datetime = data_end_datetime

        # 建立分析資料表
        self._build_self_df()
        # 建立緩存
        self._annual_return_ratio: float | None = None
        self._max_drawdown: MaxDrawdownResult | None = None
        self._earnings_volatility_ratio: float | None = None
        self._sharp_ratio: float | None = None

    def _build_self_df(self):
        # 時間資料過濾
        timestamp_column: Series = to_datetime(
            self.base_data_frame[self.timestamp_column_name],
            format=self.timestamp_format_code,
        )
        timestamp_range_filter: Series = (
            timestamp_column >= self.data_start_datetime
        ) & (timestamp_column <= self.data_end_datetime)
        temp_data_frame: DataFrame = self.base_data_frame[timestamp_range_filter]

        # 建立 DataFrame
        self.timestamp_list: List[Timestamp] = list(
            to_datetime(
                temp_data_frame[self.timestamp_column_name],
                format=self.timestamp_format_code,
            )
        )
        self.capital_list: List[float] = list(temp_data_frame[self.capital_column_name])
        self._df: DataFrame = DataFrame(
            {
                ColumnEnum.timestamp: self.timestamp_list,
                ColumnEnum.capital: self.capital_list,
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

    # 年化收益率
    def annual_return_ratio(self) -> float:
        if self._annual_return_ratio != None:
            return self._annual_return_ratio

        start_capital: float = self._df.loc[0, ColumnEnum.capital]
        end_capital: float = self._df.loc[len(self._df.index) - 1, ColumnEnum.capital]
        total_return: float = (end_capital / start_capital) - 1
        day_count: int = len(
            period_range(
                self._df[ColumnEnum.timestamp].iloc[0],
                self._df[ColumnEnum.timestamp].iloc[-1],
                freq="D",
            )
        )
        year_count: float = day_count / 365
        self._annual_return_ratio = pow(total_return + 1, 1 / year_count) - 1
        return self._annual_return_ratio

    # 最大回測
    def max_drawdown(self) -> MaxDrawdownResult:
        if self._max_drawdown != None:
            return self._max_drawdown

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
        end_timestamp: Timestamp = temp[LocalColumnEnum.timestamp]

        # 計算開始時間
        local_df = local_df[local_df[LocalColumnEnum.timestamp] <= end_timestamp]
        start_timestamp: Timestamp = local_df.sort_values(
            by=LocalColumnEnum.capital, ascending=False
        ).iloc[0][LocalColumnEnum.timestamp]

        self._max_drawdown = MaxDrawdownResult(
            max_drawdown, start_timestamp, end_timestamp
        )
        return self._max_drawdown

    # 收益波動率
    def earnings_volatility_ratio(self) -> float:
        if self._earnings_volatility_ratio != None:
            return self._earnings_volatility_ratio
        self._earnings_volatility_ratio = self._df[
            ColumnEnum.day_earnings
        ].std() * sqrt(252)
        return self._earnings_volatility_ratio

    # 夏普比率
    def sharp_ratio(self) -> float:
        if self._sharp_ratio != None:
            return self._sharp_ratio
        annual_return_ratio: float = self.annual_return_ratio()
        earnings_volatility_ratio: float = self.earnings_volatility_ratio()
        rf: float = 0.0284  # 無風險利率取 10 年期國債的到期年化收益率
        self._sharp_ratio = (annual_return_ratio - rf) / earnings_volatility_ratio
        return self._sharp_ratio
