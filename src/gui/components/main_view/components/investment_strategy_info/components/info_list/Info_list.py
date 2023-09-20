from typing import Any, List
from customtkinter import CTkScrollableFrame
from .components.info_list import Info
from ........models import InvestmentStrategyModel
from ........services import services_instance
from ........utils import TkinterUtil
from ........libs.pubsub import PubSub
from .components.info_list.components.title import (
    PUBSUB_KEY_INVESTMENT_STRATEGY_INFO_DELETE,
)
from ..header_bar import (
    PUBSUB_KEY_CLEAR_ALL_INVESTMENT_STRETAGEY_INFO,
)


class InfoList(CTkScrollableFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        self._create_widgets()
        self._build_layout()

        PubSub.subscribe(
            PUBSUB_KEY_INVESTMENT_STRATEGY_INFO_DELETE,
            self._on_investment_strategy_info_delete_handler,
        )
        PubSub.subscribe(
            PUBSUB_KEY_CLEAR_ALL_INVESTMENT_STRETAGEY_INFO,
            self._on_investment_strategy_info_delete_handler,
        )

    def destroy(self):
        PubSub.unsubscribe(
            PUBSUB_KEY_INVESTMENT_STRATEGY_INFO_DELETE,
            self._on_investment_strategy_info_delete_handler,
        )
        PubSub.unsubscribe(
            PUBSUB_KEY_CLEAR_ALL_INVESTMENT_STRETAGEY_INFO,
            self._on_investment_strategy_info_delete_handler,
        )
        return super().destroy()

    def refresh(self):
        def after_destory():
            self._create_widgets()
            self._build_layout()

        TkinterUtil.destroy_frame(self, after_destory)

    def _create_widgets(self):
        investment_strategy_list: List[
            InvestmentStrategyModel
        ] = services_instance.investment_strategy_service.get_all()

        # 投資策略訊息 Frame
        self._info_frame_list: List[Info] = [None] * len(investment_strategy_list)
        for i, investment_strategy in enumerate(investment_strategy_list):
            info_frame: Info = Info(self, investment_strategy)
            self._info_frame_list[i] = info_frame

    def _build_layout(self):
        for info_frame in self._info_frame_list:
            info_frame.pack(fill="x", pady=5)

    def _on_investment_strategy_info_delete_handler(self, name: str, _: None):
        self.refresh()
