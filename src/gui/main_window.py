from customtkinter import CTk, CTkButton, filedialog
from typing import List, Tuple
from .file_select_frame import FileSelectFrame
from .investment_strategy_form_frame import InvestmentStrategyFormFrame


class MainWindow(CTk):
    def __init__(self):
        super().__init__()
        self.geometry("600x500")
        self.title("投資策略分析 APP")

        self._widgets()
        self._layout()

    def _widgets(self):
        self.file_select_frame: FileSelectFrame = FileSelectFrame(self)

        self.investment_strategy_form_frame: InvestmentStrategyFormFrame = (
            InvestmentStrategyFormFrame(self)
        )

    def _layout(self):
        self.file_select_frame.pack(fill="x", padx=5, pady=5)
        self.investment_strategy_form_frame.pack(side="left", fill="y", padx=5, pady=5)
