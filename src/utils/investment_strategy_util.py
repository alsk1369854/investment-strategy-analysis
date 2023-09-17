from typing import List
from datetime import datetime
from pandas import DataFrame, Series, period_range


class InvestmentStrategyUtil:
    @staticmethod
    def get_day_earnings_line(
        _date_line: List[datetime],  # 日期序列
        _capital_line: List[float],  # 資本序列
    ) -> List[float]:
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

        day_earnings_line: List[float] = []
        capital_line: Series[float] = data_frame[capital_column_title]
        capital_line_count: int = capital_line.count()
        if capital_line_count > 0:
            day_earnings_line.append(0)
            for i in range(1, capital_line_count):
                yesterday_capital: float = capital_line[i - 1]
                today_capital: float = capital_line[i]

                # 日收益率 = (今日資本 - 昨日資本) / 昨日資本
                day_earnings: float = (
                    today_capital - yesterday_capital
                ) / yesterday_capital

                day_earnings_line.append(day_earnings)

        return day_earnings_line

    # 獲取年化收益率
    @staticmethod
    def get_annual_return_ratio(
        _date_line: List[datetime],  # 日期序列
        _capital_line: List[float],  # 資本序列
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
        _date_line: List[datetime],  # 日期序列
        _capital_line: List[float],  # 資本序列
    ) -> (float, datetime, datetime):  # (最大撤, 開始日期, 結束日期)
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
        max_drawdown: float = temp[drawdown_column_title]
        end_date: datetime = temp[date_column_title]

        # 計算開始時間
        data_frame = data_frame[data_frame[date_column_title] <= end_date]
        start_date: datetime = data_frame.sort_values(
            by=capital_column_title, ascending=False
        ).iloc[0][date_column_title]

        # (最大撤, 開始日期, 結束日期)
        return (max_drawdown, start_date, end_date)
