from datetime import datetime
from ..libs.cache_orm_table import cache_table_model


@cache_table_model(primary_key_column="uid")
class MaxDrawdownModel:
    uid: str
    max_drawdown_ratio: float
    start_datetime: datetime
    end_datetime: datetime
