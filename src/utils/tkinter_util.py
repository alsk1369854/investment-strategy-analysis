from typing import Optional, Callable
from tkinter import Frame


class TkinterUtil:
    @staticmethod
    def destroy_frame(
        frame: Frame,
        after_destroy: Optional[Callable[[], None]] = None,
    ):
        for widget in frame.winfo_children():
            widget.destroy()

        if after_destroy != None:
            after_destroy()
