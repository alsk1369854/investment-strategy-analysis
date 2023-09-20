from typing import Any
from customtkinter import CTkFrame, CTkButton, RIGHT
from ........libs.pubsub import PubSub
from ........services import services_instance

PUBSUB_KEY_CLEAR_ALL_INVESTMENT_STRETAGEY_INFO = (
    "PUBSUB_KEY_CLEAR_ALL_INVESTMENT_STRETAGEY_INFO"
)


class HeaderBar(CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)

        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        self._clear_all_btn: CTkButton = CTkButton(
            self,
            width=80,
            text="全部刪除",
            command=self._clear_all_btn_click_handler,
        )

    def _build_layout(self):
        self._clear_all_btn.pack(side=RIGHT, padx=5, pady=5)

    def _clear_all_btn_click_handler(self):
        services_instance.investment_strategy_service.delete_all()
        PubSub.publish(PUBSUB_KEY_CLEAR_ALL_INVESTMENT_STRETAGEY_INFO)
