from .gui import App
import matplotlib

matplotlib.rc(
    "font", family="serif", serif=["Heiti TC", "Microsoft JhengHei", "MingLiU"]
)


class Main:
    def __init__(self):
        self._app: App = App(size=(900, 350))

    def start(self):
        self._app.mainloop()
