from pandas import DataFrame, to_datetime, Series
from datetime import datetime
from ..libs.bean_factory import bean
from ..utils import PandasUtil


@bean
class BaseDataFrameService:
    def __init__(self) -> None:
        self._data_frame: DataFrame = DataFrame()

    def read_file(self, file_path: str) -> DataFrame:
        self._data_frame = PandasUtil.read_file(file_path)

    def get_data_frame(self) -> DataFrame:
        return self._data_frame

    def get_range_data(
        self,
        date_column_title: str,
        date_format_code: str,
        start_datetime: datetime,
        end_datetime: datetime,
    ) -> DataFrame:
        data_frame: DataFrame = self._data_frame.copy(deep=False)
        data_frame[date_column_title] = to_datetime(
            self._data_frame[date_column_title], format=date_format_code
        )

        date_range_filter: Series = (
            data_frame[date_column_title] >= start_datetime
        ) & (data_frame[date_column_title] <= end_datetime)

        return data_frame[date_range_filter]
