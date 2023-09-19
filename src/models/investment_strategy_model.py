from datetime import datetime
from ..libs.cache_orm_table import cache_table_model


@cache_table_model(primary_key_column="uid")
class InvestmentStrategyModel:
    uid: str
    name: str
    date_column_title: str
    start_datetime: datetime
    end_datetime: datetime
    capital_column_title: str
    annual_return_ratio: float
    max_drawdown_uid: str  # MaxDrawdownModel
    earnings_volatility_ratio: float
    sharp_ratio: float
