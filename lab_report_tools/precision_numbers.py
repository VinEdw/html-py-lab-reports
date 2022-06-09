import re

class PrecisionNumber:
    def __init__(self, value_str: str|float|int, *, sig_figs: int = None, decimal_place: int = None, absolute_error: float|int = None, relative_error: float|int = None):
        value_type = type(value_str)
        if value_type not in [str, float, int]:
            raise TypeError("PrecisionNumber *value_str* argument must be of type str|float|int")
        self._value = float(value_str)

        if sig_figs == None and decimal_place == None:
            self.sig_figs = self.count_sig_figs(str(value_str))
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
            self.absolute_error = self.get_absolute_error(str(value_str))
        elif absolute_error != None and relative_error == None:
            if type(absolute_error) not in [float, int]:
                raise TypeError("*absolute_error* argument should be a float")
            self.absolute_error = absolute_error
        elif absolute_error == None and relative_error != None:
            if type(relative_error) not in [float, int]:
                raise TypeError("*relative_error* argument should be a float")
            self.relative_error = relative_error
        else:
            raise ValueError("*absolute_error* and *relative_error* cannot both be defined")
            
        
    @property
    def value(self) -> float:
        """Get the value of the number."""
        return self._value

    @property
    def sig_figs(self) -> int:
        """Get the number of sig figs."""
    
    @property
    def decimal_place(self):
        """Get the place value of the lowest decimal place."""
    
    @property
    def absolute_error():
        """Get the absolute error of the number."""
    
    @property
    def relative_error():
        """Get the relative error of the number."""

    
    @staticmethod
    def count_sig_figs(value_str: str) -> int:
        """Count the number of significant figures (sig figs) in the input number string."""
        value = float(value_str)

    # @staticmethod
    # def get_decimal_place(value_str: str) -> int:
    #     """Get the place valueof the lowest decimal place in the input number string.
    #     The returned valueis the power 10 would need to be raised to in order to be in the proper place value."""
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