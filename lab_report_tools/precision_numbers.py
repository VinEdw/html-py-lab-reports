import math

class PrecisionNumber:
    def __init__(self, value_str: str|float|int, *, sig_figs: int = None, decimal_place: int = None, absolute_error: float|int = None, relative_error: float|int = None):
        """Initialize a PrecisionNumber with the input *value_str*.
        If *sig_figs* and *decimal_place* are both not set, then they will be inferred automatically. If one is set, that value will be used to deterine both. If both are set, then an error will be raised.
        If *absolute_error* and *relative_error* are both not set, then they will be inferred automatically. If one is set, that value will be used to deterine both. If both are set, then an error will be raised.
        """
        value_type = type(value_str)
        if value_type not in [str, float, int]:
            raise TypeError("PrecisionNumber *value_str* argument must be of type str|float|int")
        self._value = float(value_str)
        self._leading_place_value = math.floor(math.log(self._value, 10))

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
                raise TypeError("*absolute_error* argument should be a float or int")
            self.absolute_error = absolute_error
        elif absolute_error == None and relative_error != None:
            if type(relative_error) not in [float, int]:
                raise TypeError("*relative_error* argument should be a float or int")
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
        return self._sig_figs
    @property.setter
    def sig_figs(self, value: int):
        """Set the number of sig figs to the input value, and update the decimal place accordingly."""
        value = int(value)
        self._sig_figs = value
        self._decimal_place = 1 + self._leading_place_value - value
    
    @property
    def decimal_place(self) -> int:
        """Get the place value of the lowest decimal place."""
        return self._decimal_place
    @property.setter
    def decimal_place(self, value: int):
        """Set the decimal place to the input value, and update the number of sig figs accordingly."""
        value = int(value)
        self._decimal_place = value
        self._sig_figs = 1 + self._leading_place_value - value
    
    @property
    def absolute_error(self) -> float:
        """Get the absolute error of the number."""
        return self._absolute_error
    @property.setter
    def absolute_error(self, value: float|int):
        """Set the absolute error to the input value, and update the relative error accordingly."""
        value = float(value)
        self._absolute_error = value
        self._relative_error = value / self._value
    
    @property
    def relative_error(self) -> float:
        """Get the relative error of the number."""
        return self._relative_error
    @property.setter
    def relative_error(self, value: float|int):
        """Set the relative error to the input value, and update the absolute error accordingly."""
        value = float(value)
        self._absolute_error = value
        self._relative_error = value * self._value

    
    @staticmethod
    def count_sig_figs(value_str: str) -> int:
        """Count the number of significant figures (sig figs) in the input number string."""
        value = float(value_str)
        value_str = value_str.strip().upper()
        value_str = value_str.replace("_", "")
        value_str = value_str.replace("+", "")
        value_str = value_str.replace("-", "")
        if "E" in value_str:
            num_part = value_str.split("E")[0]
            return PrecisionNumber.count_sig_figs(num_part)
        if "." in value_str:
            sf_count = 0
            pre_decimal_point, post_decimal_point = value_str.split(".")
            pre_decimal_point = pre_decimal_point.lstrip("0")
            sf_count += len(pre_decimal_point)
            if len(pre_decimal_point) == 0:
                sf_count += len(post_decimal_point.lstrip("0"))
            else:
                sf_count += len(post_decimal_point)
            return sf_count
        else:
            return len(value_str.strip("0"))

    @staticmethod
    def get_decimal_place(value_str: str) -> int:
        """Get the place value of the lowest decimal place in the input number string.
        The returned value is the power 10 would need to be raised to in order to be in the proper place value.
        """
        value = float(value_str)
        leading_place_value = math.floor(math.log(value, 10))
        sf_count = PrecisionNumber.count_sig_figs(value_str)
        return 1 + leading_place_value - sf_count
    
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