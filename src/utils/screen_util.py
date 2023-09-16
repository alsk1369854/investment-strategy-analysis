from typing import Tuple
from screeninfo import get_monitors


class ScreenUtil:
    @staticmethod
    def get_primary_screen_size() -> Tuple[int, int]:
        for monitor in get_monitors():
            if monitor.is_primary == True:
                return (monitor.width, monitor.height)
