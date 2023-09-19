from typing import List, Optional
from ..libs.bean_factory import bean
from ..libs.cache_orm_table import CacheOrmTable, Session
from ..models import InvestmentStrategyModel


@bean
class InvestmentStrategyDAO:
    def get_one(
        self,
        filter_model: Optional[InvestmentStrategyModel] = None,
    ) -> InvestmentStrategyModel:
        session: Session = CacheOrmTable.get_session(InvestmentStrategyModel)

        if filter_model != None:
            filter_dict = filter_model.__dict__
            session = session.filter_by(**filter_dict)

        return session.one()

    def get_list(
        self,
        filter_model: Optional[InvestmentStrategyModel] = None,
    ) -> List[InvestmentStrategyModel]:
        session: Session = CacheOrmTable.get_session(InvestmentStrategyModel)

        if filter_model != None:
            filter_dict = filter_model.__dict__
            session = session.filter_by(**filter_dict)

        return session.list()

    def delete(
        self,
        filter_model: Optional[InvestmentStrategyModel] = None,
    ) -> None:
        session: Session = CacheOrmTable.get_session(InvestmentStrategyModel)

        if filter_model != None:
            filter_dict = filter_model.__dict__
            session = session.filter_by(**filter_dict)

        return session.delete()

    def create(
        self,
        data_model: InvestmentStrategyModel,
    ) -> None:
        CacheOrmTable.get_session(InvestmentStrategyModel).add(data_model)
