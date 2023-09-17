from .views import MainWindow


class Main:
    def __init__(self):
        self.main_window: MainWindow = MainWindow(size=(900, 350))

    def start(self):
        self.main_window.mainloop()
