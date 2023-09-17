from typing import Any, Callable, Optional, Tuple
from customtkinter import CTkToplevel
from tkcalendar import Calendar
from datetime import datetime
from .....utils import ScreenUtil

DATE_PATTERN = "YYYY/mm/dd"
DATE_PICKER_FORMAT_CODE: str = "%Y/%m/%d"


class DatePickerTopWindow(CTkToplevel):
    def __init__(
        self,
        master: Any,
        selected_handler: Callable[[str], None],
        title: Optional[str] = "日期選擇器",
        mindate: Optional[datetime] = None,
        maxdate: Optional[datetime] = None,
    ):
        super().__init__(master)
        self.selected_handler: Callable[[str], None] = selected_handler

        self.title(title)
        screen_size: Tuple[int, int] = ScreenUtil.get_primary_screen_size()
        self.geometry(f"+{int(screen_size[0]/2 -100)}+{int(screen_size[1]/2 -50)}")

        self._date_picker: Calendar = Calendar(
            self,
            selectmode="day",
            date_pattern=DATE_PATTERN,
            showweeknumbers=False,
            showothermonthdays=False,
        )
        if mindate != None:
            self._date_picker.configure(mindate=mindate)
        if maxdate != None:
            self._date_picker.configure(maxdate=maxdate)

        self._date_picker.bind(
            "<<CalendarSelected>>", self._date_picker_selecet_handler
        )
        self._date_picker.pack(padx=10, pady=10)

    def _date_picker_selecet_handler(self, even):
        selected_date: str = self._date_picker.get_date()
        self.selected_handler(selected_date)
