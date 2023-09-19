from pandas import Series
from datetime import datetime
from ..libs.bean_factory import bean
from ..models import MaxDrawdownModel
from ..daos import MaxDrawdownDAO
from ..utils import InvestmentStrategyUtil, BasicUtil


@bean
class MaxDrawdownService:
    _max_drawdown_dao: MaxDrawdownDAO

    def get_one_by_uid(self, uid: str) -> MaxDrawdownModel:
        filter_model: MaxDrawdownModel = MaxDrawdownModel()
        filter_model.uid = uid
        return self._max_drawdown_dao.get_one(filter_model)

    def selete_by_uid(self, uid: str) -> None:
        filter_model: MaxDrawdownModel = MaxDrawdownModel()
        filter_model.uid = uid
        return self._max_drawdown_dao.delete(filter_model)

    def create(
        self,
        date_line: Series,  # 日期序列
        capital_line: Series,  # 資本序列 float
    ) -> MaxDrawdownModel:
        data_model: MaxDrawdownModel = MaxDrawdownModel()
        data_model.uid = BasicUtil.get_general_uuid()
        (
            max_drawdown_ratio,
            start_datetime,
            end_datetime,
        ) = InvestmentStrategyUtil.max_drawdown(date_line, capital_line)
        data_model.max_drawdown_ratio = max_drawdown_ratio
        data_model.start_datetime = start_datetime
        data_model.end_datetime = end_datetime

        # create to table
        self._max_drawdown_dao.create(data_model)
        return data_model
