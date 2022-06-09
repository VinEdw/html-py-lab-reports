import re

class PrecisionNumber:
    def __init__(self, value: str|float|int, *, sig_figs: int = None, decimal_place: int = None, absolute_error: float = None, relative_error: float = None):
        value_type = type(value)
        if not ((value_type is int) or (value_type is float) or (value_type is str)):
            raise TypeError("PrecisionNumber value argument must be of type str|float|int")
        self._value = float(value)

        if sig_figs == None and decimal_place == None:
            if value_type is not str:
                raise ValueError("*sig_figs* and *decimal_place* cannot both be None if *value* is not a str")
            self.sig_figs = self.count_sig_figs(value)
        elif sig_figs != None and decimal_place == None:
            if type(sig_figs) is not int:
                raise TypeError("*sig_figs* argument should be an int")
            self.sig_figs = sig_figs
        elif sig_figs == None and decimal_place != None:
            if type(decimal_place) is not int:
                raise TypeError("*decimal_place* argument should be an int")
            self.decimal_place = decimal_place
        else:
            raise ValueError("*sig_figs* and *decimal_place* cannot both be defined")

        if absolute_error == None and relative_error == None:
            if value_type is not str:
                raise ValueError("*absolute_error* and *relative_error* cannot both be None if *value* is not a str")
            self.absolute_error = self.get_absolute_error(value)
        elif absolute_error != None and relative_error == None:
            if type(absolute_error) is not float:
                raise TypeError("*absolute_error* argument should be a float")
            self.absolute_error = absolute_error
        elif absolute_error == None and relative_error != None:
            if type(relative_error) is not float:
                raise TypeError("*relative_error* argument should be a float")
            self.relative_error = relative_error
        else:
            raise ValueError("*absolute_error* and *relative_error* cannot both be defined")
            
        
    @property
    def value(self):
        """Get the number's value."""
        return self._value

    
    @staticmethod
    def count_sig_figs(value_str: str) -> int:
        """Count the number of significant figures (sig figs) in the input number string."""
        value = float(value_str)

    # @staticmethod
    # def get_decimal_place(value_str: str) -> int:
    #     """Get the place value of the lowest decimal place in the input number string.
    #     The returned value is the power 10 would need to be raised to in order to be in the proper place value."""
    #     value = float(value_str)
    
    @staticmethod
    def get_absolute_error(value_str: str) -> int:
        """Get the absolute error of the input number string."""
        value = float(value_str)

    # @staticmethod
    # def get_relative_error(value_str: str) -> int:
    #     """Get the relative error of the input number string."""
    #     value = float(value_str)

if __name__ == "__main__":
    import unittest

    class TestSigFigCounter(unittest.TestCase):
        """Test if PrecisionNumber.count_sig_figs() works properly."""
        
        def test_no_decmial_point(self):
            """Test numbers that do not contain a decimal point."""
            self.assertNotEqual(PrecisionNumber.count_sig_figs("120"), None)

    unittest.main()