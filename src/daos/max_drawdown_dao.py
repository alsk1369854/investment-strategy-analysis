from typing import Optional, List
from ..libs.bean_factory import bean
from ..libs.cache_orm_table import Session, CacheOrmTable
from ..models import MaxDrawdownModel


@bean
class MaxDrawdownDAO:
    def get_one(
        self,
        filter_model: Optional[MaxDrawdownModel] = None,
    ) -> MaxDrawdownModel:
        session: Session = CacheOrmTable.get_session(MaxDrawdownModel)

        if filter_model != None:
            filter_dict = filter_model.__dict__
            session = session.filter_by(**filter_dict)

        return session.one()

    def get_list(
        self,
        filter_model: Optional[MaxDrawdownModel] = None,
    ) -> List[MaxDrawdownModel]:
        session: Session = CacheOrmTable.get_session(MaxDrawdownModel)

        if filter_model != None:
            filter_dict = filter_model.__dict__
            session = session.filter_by(**filter_dict)

        return session.list()

    def delete(
        self,
        filter_model: Optional[MaxDrawdownModel] = None,
    ) -> None:
        session: Session = CacheOrmTable.get_session(MaxDrawdownModel)

        if filter_model != None:
            filter_dict = filter_model.__dict__
            session = session.filter_by(**filter_dict)

        return session.delete()

    def create(
        self,
        data_model: MaxDrawdownModel,
    ) -> None:
        CacheOrmTable.get_session(MaxDrawdownModel).add(data_model)
