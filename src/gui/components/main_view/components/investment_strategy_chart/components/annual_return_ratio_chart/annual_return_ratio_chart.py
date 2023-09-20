from customtkinter import CTkFrame, CTkCanvas
from typing import Any
from tkinter import Canvas
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from ........services import services_instance


class AnnualReturnRatioChart(CTkFrame):
    def __init__(self, master: Any):
        super().__init__(master)
        self._create_widgets()
        self._build_layout()

    def _create_widgets(self):
        figure: Figure = (
            services_instance.investment_strategy_service.get_annual_return_ratio_chart()
        )
        figure_canvas_agg: FigureCanvasTkAgg = FigureCanvasTkAgg(figure, self)
        figure_canvas_agg.draw()
        self._figure_canvas: Canvas = figure_canvas_agg.get_tk_widget()

    def _build_layout(self):
        self._figure_canvas.pack(fill="both", expand=True)
