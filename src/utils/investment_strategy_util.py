from typing import Tuple
from datetime import datetime
from pandas import DataFrame, Series, period_range
from math import sqrt


class InvestmentStrategyUtil:
    @staticmethod
    def get_day_earnings_line(
        _date_line: Series[datetime],  # 日期序列
        _capital_line: Series[float],  # 資本序列
    ) -> Series[float]:
        # create DataFrame
        date_column_title: str = "date_column_title"
        capital_column_title: str = "capital_column_title"
        data_frame: DataFrame = DataFrame(
            {
                date_column_title: _date_line,
                capital_column_title: _capital_line,
            }
        )
        data_frame.sort_values(by=date_column_title, inplace=True)
        data_frame.reset_index(drop=True, inplace=True)

        # 計算
        # 昨日資本列
        prev_capital_column_title: str = "prev_capital_column_title"
        data_frame[prev_capital_column_title] = data_frame[capital_column_title].shift(
            1
        )

        # 日收益率 = (今日資本 - 昨日資本) / 昨日資本
        day_earnings_column_title: str = "day_earnings_column_title"
        data_frame[day_earnings_column_title] = (
            data_frame[capital_column_title] - data_frame[prev_capital_column_title]
        ) / data_frame[prev_capital_column_title]

        # 将日收益率列转换为列表并返回
        day_earnings_line: Series[float] = data_frame[day_earnings_column_title]
        return day_earnings_line

    # 獲取年化收益率
    @staticmethod
    def get_annual_return_ratio(
        _date_line: Series[datetime],  # 日期序列
        _capital_line: Series[float],  # 資本序列
    ) -> float:
        # 創建 DataFrame
        date_column_title: str = "date_column_title"
        capital_column_title: str = "capital_column_title"
        data_frame: DataFrame = DataFrame(
            {
                date_column_title: _date_line,
                capital_column_title: _capital_line,
            }
        )
        data_frame.sort_values(by=date_column_title, inplace=True)
        data_frame.reset_index(drop=True, inplace=True)

        # 計算
        start_capital: float = data_frame.loc[0, capital_column_title]
        end_capital: float = data_frame.loc[
            len(data_frame.index) - 1, capital_column_title
        ]
        total_return: float = (end_capital / start_capital) - 1
        day_count: int = len(
            period_range(
                data_frame[data_frame].iloc[0],
                data_frame[data_frame].iloc[-1],
                freq="D",
            )
        )
        year_count: float = day_count / 365
        annual_return_ratio = pow(total_return + 1, 1 / year_count) - 1
        return annual_return_ratio

    # 最大回測
    @staticmethod
    def max_drawdown(
        _date_line: Series[datetime],  # 日期序列
        _capital_line: Series[float],  # 資本序列
    ) -> Tuple[float, datetime, datetime]:  # (最大撤, 開始日期, 結束日期)
        # 創建 DataFrame
        date_column_title: str = "date_column_title"
        capital_column_title: str = "capital_column_title"
        data_frame: DataFrame = DataFrame(
            {
                date_column_title: _date_line,
                capital_column_title: _capital_line,
            }
        )
        data_frame.sort_values(by=date_column_title, inplace=True)
        data_frame.reset_index(drop=True, inplace=True)

        # 計算當日之前的張戶最大價值
        max_capital_before_column_title: str = "max_capital_before_column_title"
        data_frame[max_capital_before_column_title] = data_frame[
            capital_column_title
        ].cummax()

        # 計算當日回撤
        drawdown_column_title: str = "drawdown_column_title"
        data_frame[drawdown_column_title] = (
            data_frame[capital_column_title]
            / data_frame[max_capital_before_column_title]
            - 1
        )

        # 計算最大回撤和結束時間
        temp: DataFrame = data_frame.sort_values(by=drawdown_column_title).iloc[0][
            [date_column_title, drawdown_column_title]
        ]
        max_drawdown_ratio: float = temp[drawdown_column_title]
        end_datetime: datetime = temp[date_column_title]

        # 計算開始時間
        data_frame = data_frame[data_frame[date_column_title] <= end_datetime]
        start_datetime: datetime = data_frame.sort_values(
            by=capital_column_title, ascending=False
        ).iloc[0][date_column_title]

        # (最大撤, 開始日期, 結束日期)
        return (max_drawdown_ratio, start_datetime, end_datetime)

    # 收益波動率
    @staticmethod
    def get_earnings_volatility_ratio(
        _date_line: Series[datetime],  # 日期序列
        _capital_line: Series[float],  # 資本序列
    ) -> float:
        day_earnings_line: Series[float] = InvestmentStrategyUtil.get_day_earnings_line(
            _date_line, _capital_line
        )
        # 計算
        earnings_vaolatility_ratio: float = day_earnings_line.std() * sqrt(252)
        return earnings_vaolatility_ratio

    # 夏普比率
    @staticmethod
    def get_sharp_ratio(
        _date_line: Series[datetime],  # 日期序列
        _capital_line: Series[float],  # 資本序列
    ) -> float:
        annual_return_ratio: float = InvestmentStrategyUtil.get_annual_return_ratio(
            _date_line, _capital_line
        )
        earnings_volatility_ratio: float = (
            InvestmentStrategyUtil.get_earnings_volatility_ratio(
                _date_line, _capital_line
            )
        )

        rf: float = 0.0284  # 無風險利率取 10 年期國債的到期年化收益率
        sharp_ratio: float = (annual_return_ratio - rf) / earnings_volatility_ratio
        return sharp_ratio
