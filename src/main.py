from .gui import App


class Main:
    def __init__(self):
        self._app: App = App(size=(900, 350))

    def start(self):
        self._app.mainloop()
