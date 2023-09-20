from typing import List
from datetime import datetime
from pandas import DataFrame, Series, Timestamp, to_datetime
from matplotlib import pyplot
from .base_data_frame_service import BaseDataFrameService
from .max_drawdown_service import MaxDrawdownService
from ..libs.bean_factory import bean
from ..models import InvestmentStrategyModel, MaxDrawdownModel
from ..daos import InvestmentStrategyDAO
from ..utils import InvestmentStrategyUtil, UuidUtil


@bean
class InvestmentStrategyService:
    _investment_strategy_dao: InvestmentStrategyDAO
    _base_data_frame_service: BaseDataFrameService
    _max_drawdown_service: MaxDrawdownService

    def get_all(self) -> List[InvestmentStrategyModel]:
        return self._investment_strategy_dao.get_list()

    def delete_by_uid(self, uid: str) -> None:
        filter_model: InvestmentStrategyModel = InvestmentStrategyModel()
        filter_model.uid = uid
        self._investment_strategy_dao.delete(filter_model)

    def delete_all(self) -> None:
        self._investment_strategy_dao.delete()

    def create(
        self,
        name: str,
        date_column_title: str,
        date_format_code: str,
        capital_column_title: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> InvestmentStrategyModel:
        investment_strategy: InvestmentStrategyModel = InvestmentStrategyModel()
        investment_strategy.uid = UuidUtil.get_general_uuid()
        investment_strategy.name = name
        investment_strategy.date_column_title = date_column_title
        investment_strategy.capital_column_title = capital_column_title
        investment_strategy.start_datetime = start_datetime
        investment_strategy.end_datetime = end_datetime

        # 建立計算所得數據
        base_data_frame: DataFrame = self._base_data_frame_service.get_range_data(
            date_column_title=date_column_title,
            date_format_code=date_format_code,
            start_datetime=start_datetime,
            end_datetime=end_datetime,
        )
        date_line: Series[datetime] = base_data_frame[date_column_title]
        capital_line: Series[float] = base_data_frame[capital_column_title]
        # 獲取年化收益率
        investment_strategy.annual_return_ratio = (
            InvestmentStrategyUtil.get_annual_return_ratio(date_line, capital_line)
        )
        investment_strategy.earnings_volatility_ratio = (
            InvestmentStrategyUtil.get_earnings_volatility_ratio(
                date_line, capital_line
            )
        )
        investment_strategy.sharp_ratio = InvestmentStrategyUtil.get_sharp_ratio(
            date_line, capital_line
        )

        max_drawdown: MaxDrawdownModel = self._max_drawdown_service.create(
            date_line, capital_line
        )
        investment_strategy.max_drawdown_uid = max_drawdown.uid

        # create to table
        self._investment_strategy_dao.create(investment_strategy)

        return investment_strategy

    def get_annual_return_ratio_chart(self) -> pyplot.Figure:
        investment_stragety_list: List[InvestmentStrategyModel] = self.get_all()
        investment_stragety_list_len: int = len(investment_stragety_list)
        y_axis: List[str] = [""] * investment_stragety_list_len
        x_axis: List[int] = [0] * investment_stragety_list_len
        for i, investment_stragety in enumerate(investment_stragety_list):
            y_axis[i] = investment_stragety.name
            x_axis[i] = int(investment_stragety.annual_return_ratio * 100)

        fig, ax = pyplot.subplots()
        ax.barh(y_axis, x_axis)
        ax.set_title("年化收益率")
        ax.set_xlabel("百分比")
        ax.set_xlabel("策略名稱")
        return fig
