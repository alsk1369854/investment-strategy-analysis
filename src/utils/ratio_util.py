class RatioUtil:
    @staticmethod
    def parse_to_percent_str(num: float) -> str:
        percent_str: str = "%.2f" % (num * 100.0)
        return f"{percent_str}%"
