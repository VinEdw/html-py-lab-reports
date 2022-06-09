import re

class PrecisionNumber:
    def __init__(self, value: str|float|int, *, sig_figs: int, decimal_place: int, absolute_error: float, relative_error: float):
        value_type = type(value)
        if (value_type is int) or (value_type is float):
            self._value = value
        elif value_type is str:
            self._value = float(value)
        else:
            raise TypeError("PrecisionNumber value argument must be of type str|float|int")
        
    @property
    def value(self):
        """Get the number's value."""
        return self._value

    
    @staticmethod
    def count_sig_figs(value_str: str) -> int:
        value = float(value_str)


if __name__ == "__main__":
    import unittest

    class TestSigFigCounter(unittest.TestCase):
        
        def no_decmial_point(self):
            self.assertEqual(PrecisionNumber.count_sig_figs("120"), 2)

    unittest.main()