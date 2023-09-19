from typing import Dict, TypeVar, Type, List, Generic, Self, Any, Callable, Optional
from pandas import DataFrame, Series, concat
from .utils import BasicUtil

T = TypeVar("T")


class Table(Generic[T]):
    def __init__(self, primary_key_column: str, columns: List[str]):
        self._data_frame: DataFrame = DataFrame(columns=columns)
        self._primary_key_column: str = primary_key_column
        self._data_frame.set_index(primary_key_column, inplace=True)

    @property
    def primary_key_column_name(self) -> str:
        return self._primary_key_column

    def get_data_frame(self) -> DataFrame:
        return self._data_frame

    def drop(
        self,
        *args,
        **keyargs,
    ) -> None:
        self._data_frame.drop(inplace=True, *args, **keyargs)

    def append(self, data_mode_list: List[T]):
        for data_mode in data_mode_list:
            data: Dict[str, List[Any]] = BasicUtil.get_create_data_frame_data(data_mode)
            new_row: DataFrame = DataFrame(data)
            new_row.set_index(self.primary_key_column_name, inplace=True)
            self._data_frame = concat([self._data_frame, new_row.dropna()])


class Session(Generic[T]):
    def __init__(self, table_model_class: Type[T], table: Table[T]) -> None:
        self._table_model_class: Type[T] = table_model_class
        self._table: Table[T] = table
        self._filtered_data_frame: DataFrame = self._table.get_data_frame()

    def filter_by(self, **keyargs) -> Self:
        for key in keyargs:
            value: Any = keyargs[key]

            if key == self._table.primary_key_column_name:
                filter: DataFrame = self._filtered_data_frame.index == value
                self._filtered_data_frame = self._filtered_data_frame[filter]
                break

            filter: DataFrame = self._filtered_data_frame[key] == value
            self._filtered_data_frame = self._filtered_data_frame[filter]

        return self

    def add(self, model: T) -> None:
        if not isinstance(model, self._table_model_class):
            raise TypeError(
                f"{model.__class__} is not isinstance {self._table_model_class.__name__}"
            )

        self._table.append([model])

    def delete(self) -> None:
        self._table = self._table.drop(self._filtered_data_frame.index)

    def one(self) -> T:
        row: Series = self._filtered_data_frame.iloc[0]
        return self._build_one_model(row)

    def list(self) -> List[T]:
        data_frame: DataFrame = self._filtered_data_frame
        return self._build_list_model(data_frame)

    def _build_one_model(self, row: Series) -> T:
        model: T = self._table_model_class()

        # set primary key
        primary_key_value: Any = row.name
        setattr(model, self._table.primary_key_column_name, primary_key_value)

        # set other data
        column_title_list: List[str] = row.index.to_list()
        for column_title in column_title_list:
            setattr(model, column_title, row[column_title])
        return model

    def _build_list_model(self, data_frame: DataFrame) -> List[T]:
        row_len: int = len(data_frame)
        model_list: List[T] = [None] * row_len
        for i in range(row_len):
            row: Series = data_frame.iloc[i]
            model: T = self._build_one_model(row)
            model_list[i] = model

        return model_list


class CacheOrmTable:
    _table_dict: Dict[Type[T], Table[T]] = {}

    @staticmethod
    def add_table_model_class(table_model_class: Type[T], primary_key: str) -> None:
        columns: List[str] = [
            key for key in BasicUtil.get_class_annotations(table_model_class)
        ]
        CacheOrmTable._table_dict[table_model_class] = Table(
            primary_key_column=primary_key,
            columns=columns,
        )

    @staticmethod
    def get_session(table_model_class: Type[T]) -> Session[T]:
        table: Table[T] = CacheOrmTable._table_dict[table_model_class]
        return Session(table_model_class, table)

    @staticmethod
    def _update_table(table_model_class: Type[T], new_table: Table[T]) -> None:
        CacheOrmTable._table_dict[table_model_class] = new_table


def cache_table_model(primary_key_column: str) -> Callable[[Type[T]], Type[T]]:
    def decorate(table_model_class: Type[T]) -> Type[T]:
        CacheOrmTable.add_table_model_class(table_model_class, primary_key_column)
        return table_model_class

    return decorate
