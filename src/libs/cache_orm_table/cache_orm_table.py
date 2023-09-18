from typing import Dict, TypeVar, Type, List, Generic, Self, Any, Callable
import pandas as pd
from .utils import BasicUtil

T = TypeVar("T")


class Table(pd.DataFrame, Generic[T]):
    def __init__(self, primary_key: str, *args, **keyargs):
        super().__init__(*args, **keyargs)
        self.primary_key: str = primary_key
        self.set_index(primary_key, inplace=True)


class Session(Generic[T]):
    def __init__(self, table_model_class: Type[T], table: Table[T]) -> None:
        self._table_model_class: Type[T] = table_model_class
        self._table: Table = table
        self._filter_table: Table = self._table

    def filter_by(self, **keyargs) -> Self:
        for key in keyargs:
            value: Any = keyargs[key]

            if key == self._table.primary_key:
                self._filter_table = self._filter_table.loc[key]
                break

            filter = self._filter_table[key] == value
            self._filter_table = self._filter_table[filter]

    def add(self, model: T) -> None:
        if isinstance(model, self._table_model_class):
            data: Dict[str, Any] = model.__dict__
            index: Any = data[self._table.primary_key]
            del data[self._table.primary_key]

            new_row: pd.DataFrame = pd.DataFrame(data, index=[index])
            self._table = pd.concat([self._table, new_row])
            CacheOrmTable._update_table(self._table_model_class, self._table)

        raise TypeError(f"{model} is not isinstance {self._table_model_class}")

    def delete(self) -> None:
        self._table = self._table.drop(self._filter_table.index, inplace=True)

    def one(self) -> T:
        row: pd.Series = self._filter_table.iloc[0]
        return self._build_one_model(row)

    def list(self) -> List[T]:
        table: Table[T] = self._filter_table
        return self._build_list_model(table)

    def _build_one_model(self, row: pd.Series) -> T:
        model: T = T()
        column_title_list: List[str] = row.index.to_list()
        for column_title in column_title_list:
            setattr(model, column_title, row[column_title])
        return model

    def _build_list_model(self, table: Table[T]) -> List[T]:
        row_len: int = len(table)
        model_list: List[T] = [None] * row_len
        for i in range(row_len):
            index: pd.Index = table.index[i]
            model: T = self._build_one_model(table.loc[index])
            model_list[i] = model

        return model_list


class CacheOrmTable:
    _table_dict: Dict[Type[T], Table[T]]

    @staticmethod
    def add_table_model_class(table_model_class: Type[T], primary_key: str) -> None:
        columns: List[str] = [
            key for key in BasicUtil.get_class_annotations(table_model_class)
        ]
        CacheOrmTable._table_dict[table_model_class] = Table(
            columns=columns, index=primary_key
        )

    @staticmethod
    def get_session(table_model_class: Type[T]) -> Session[T]:
        table: Table[T] = CacheOrmTable._table_dict[table_model_class]
        return Session(table)

    @staticmethod
    def _update_table(table_model_class: Type[T], new_table: Table[T]) -> None:
        CacheOrmTable._table_dict[table_model_class] = new_table


def cache_table_model(primay_key: str) -> Callable[[Type[T]], Type[T]]:
    def decorate(table_model_class: Type[T]) -> Type[T]:
        CacheOrmTable.add_table_model_class(table_model_class, primay_key)
        return table_model_class

    return decorate
