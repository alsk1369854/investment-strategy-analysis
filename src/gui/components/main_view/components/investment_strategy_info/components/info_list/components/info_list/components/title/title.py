from typing import Any
from customtkinter import CTkFrame, CTkLabel, CTkImage, LEFT, RIGHT
from ............models import InvestmentStrategyModel
from ............utils import IconUtil
from ............services import services_instance
from ............libs.pubsub import PubSub


PUBSUB_KEY_INVESTMENT_STRATEGY_INFO_DELETE = (
    "PUBSUB_KEY_INVESTMENT_STRATEGY_INFO_DELETE"
)


class Title(CTkFrame):
    def __init__(
        self,
        master: Any,
        investment_strategy: InvestmentStrategyModel,
    ):
        super().__init__(master)
        self._investment_strategy: InvestmentStrategyModel = investment_strategy

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        # 策略名稱
        investment_strategy_name: str = self._investment_strategy.name
        self._investment_strategy_name_label: CTkLabel = CTkLabel(
            self, text=f"策略名稱: {investment_strategy_name}"
        )

        delete_img = CTkImage(
            light_image=IconUtil.get_icon("clear_light"),
            dark_image=IconUtil.get_icon("clear_dark"),
            size=(15, 15),
        )
        self._delete_label: CTkLabel = CTkLabel(self, image=delete_img, text="")
        self._delete_label.bind("<Button-1>", self._delete_label_click_handler)

    def _build_layout(self):
        self._investment_strategy_name_label.pack(side=LEFT, padx=5, pady=5)
        self._delete_label.pack(side=RIGHT, padx=5, pady=5)

    def _delete_label_click_handler(self, event: Any):
        investment_strategy_uid: str = self._investment_strategy.uid
        services_instance.investment_strategy_service.delete_by_uid(
            investment_strategy_uid
        )
        PubSub.publish(PUBSUB_KEY_INVESTMENT_STRATEGY_INFO_DELETE)
