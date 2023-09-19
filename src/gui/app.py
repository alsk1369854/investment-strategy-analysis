from customtkinter import CTk
from typing import Tuple
from .components.main_view import MainView
from .components.file_select_bar import FileSelectBar
from .components.create_investment_strategy_form import CreateInvestmentStrategyForm
from ..utils import ScreenUtil
from ..models import InvestmentStrategyModel
from ..services import services_instance


class App(CTk):
    def __init__(self, size: Tuple[int, int]):
        super().__init__()
        self.title("投資策略分析 APP")
        screen_size: Tuple[int, int] = ScreenUtil.get_primary_screen_size()
        self.geometry(
            f"{size[0]}x{size[1]}+{int(screen_size[0]/2 - (size[0]/2))}+{int(screen_size[1]/2 -(size[1]/2))}"
        )
        self.minsize(width=size[0], height=size[1])

        self._create_widgets()
        self._build_layout()

    def destroy(self):
        print("test")
        return super().destroy()

    def _create_widgets(self):
        # top
        self._file_select_bar: FileSelectBar = FileSelectBar(
            self, on_selected=self._on_file_seleted
        )

        # main
        self._main_tab_view: MainView = MainView(self)

        # left side
        self._create_investment_strategy_form_frame: CreateInvestmentStrategyForm = (
            CreateInvestmentStrategyForm(
                self, on_submit=self._on_investment_strategy_form_submit
            )
        )

    def _build_layout(self):
        # top
        self._file_select_bar.pack(fill="x", padx=5, pady=5)
        # left side
        self._create_investment_strategy_form_frame.pack(
            side="left", fill="y", padx=5, pady=5
        )
        # main
        self._main_tab_view.pack(expand=True, fill="both", padx=5, pady=5)

    def _on_investment_strategy_form_submit(
        self, investment_strategy: InvestmentStrategyModel
    ):
        self._main_tab_view.refresh_tab_strategy_info()

    def _on_file_seleted(self, file_path: str):
        services_instance.investment_strategy_service.delete_all()
        self._create_investment_strategy_form_frame.refresh()
        self._main_tab_view.refresh()
