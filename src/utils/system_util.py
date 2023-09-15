import sys


class SystemUtil:
    @staticmethod
    def is_linux() -> bool:
        # 包含 linux 與 linux2 的情況
        return sys.platform.startswith("linux")

    def is_macOS() -> bool:
        return sys.platform.startswith("darwin")

    def is_windows() -> bool:
        return sys.platform.startswith("win32")
