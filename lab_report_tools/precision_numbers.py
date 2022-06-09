import re

class PrecisionNumber:
    def __init__(self, value_str: str, *, sig_figs: int, decimal_place: int, absolute_error: float, relative_error: float):
        self.value_str = value_str
        self.value = float(value_str)
    
    @staticmethod
    def count_sig_figs(value_str: str) -> int:
        value = float(value_str)


if __name__ == "__main__":
    import unittest

    class TestSigFigCounter(unittest.TestCase):
        
        def no_decmial_point(self):
            self.assertEqual(PrecisionNumber.count_sig_figs("120"), 3)

    unittest.main()