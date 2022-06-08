class PresisonNumber:
    def __init__(self, value_str: str, *, sigFigs: int, decimalPlace: int, absoluteError: float, relativeError: float):
        self.value_str = value_str
        self.value = float(value_str)


if __name__ == "__main__":
    pass