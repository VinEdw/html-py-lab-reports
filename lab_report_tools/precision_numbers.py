import math

class PrecisionNumber:
    def __init__(self, value_str: str|float|int, *, sig_figs: int = None, decimal_place: int = None, absolute_error: float|int = None, relative_error: float|int = None):
        """Initialize a PrecisionNumber with the input *value_str*.
        If *sig_figs* and *decimal_place* are both not set, then they will be inferred automatically. If one is set, that value will be used to deterine both. If both are set, then an error will be raised.
        If *absolute_error* and *relative_error* are both not set, then they will be inferred automatically. If one is set, that value will be used to deterine both. If both are set, then an error will be raised.
        """
        if not isinstance(value_str, (str, float, int)):
            raise TypeError("PrecisionNumber *value_str* argument must be of type str|float|int")
        self._value = float(value_str)
        self._leading_place_value = math.floor(math.log(self._value, 10))

        if sig_figs == None and decimal_place == None:
            self.sig_figs = self.count_sig_figs(str(value_str))
        elif sig_figs != None and decimal_place == None:
            if not isinstance(sig_figs, int):
                raise TypeError("*sig_figs* argument should be an int")
            self.sig_figs = sig_figs
        elif sig_figs == None and decimal_place != None:
            if not isinstance(decimal_place, int):
                raise TypeError("*decimal_place* argument should be an int")
            self.decimal_place = decimal_place
        else:
            raise ValueError("*sig_figs* and *decimal_place* cannot both be defined")

        if absolute_error == None and relative_error == None:
            self.absolute_error = self.get_absolute_error(str(value_str))
        elif absolute_error != None and relative_error == None:
            if not isinstance(absolute_error, (float, int)):
                raise TypeError("*absolute_error* argument should be a float or int")
            self.absolute_error = absolute_error
        elif absolute_error == None and relative_error != None:
            if not isinstance(relative_error, (float, int)):
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
    @sig_figs.setter
    def sig_figs(self, value: int):
        """Set the number of sig figs to the input value, and update the decimal place accordingly."""
        value = int(value)
        self._sig_figs = value
        self._decimal_place = 1 + self._leading_place_value - value
    
    @property
    def decimal_place(self) -> int:
        """Get the place value of the lowest decimal place."""
        return self._decimal_place
    @decimal_place.setter
    def decimal_place(self, value: int):
        """Set the decimal place to the input value, and update the number of sig figs accordingly."""
        value = int(value)
        self._decimal_place = value
        self._sig_figs = 1 + self._leading_place_value - value
    
    @property
    def absolute_error(self) -> float:
        """Get the absolute error of the number."""
        return self._absolute_error
    @absolute_error.setter
    def absolute_error(self, value: float|int):
        """Set the absolute error to the input value, and update the relative error accordingly."""
        value = float(value)
        self._absolute_error = value
        self._relative_error = value / self._value
    
    @property
    def relative_error(self) -> float:
        """Get the relative error of the number."""
        return self._relative_error
    @relative_error.setter
    def relative_error(self, value: float|int):
        """Set the relative error to the input value, and update the absolute error accordingly."""
        value = float(value)
        self._absolute_error = value
        self._relative_error = value * self._value


    def __add__(self, value, /):
        """When two numbers are added together, the lower decimal place is used in the result and the absolute errors add together."""
        value_type = type(value)

    
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
    def get_absolute_error(value_str: str) -> float:
        """Get the absolute error of the input number string."""
        value = float(value_str)
        decimal_place = PrecisionNumber.get_decimal_place(value_str)
        return 10**decimal_place

    @staticmethod
    def get_relative_error(value_str: str) -> float:
        """Get the relative error of the input number string."""
        value = float(value_str)
        absolute_error = PrecisionNumber.get_absolute_error(value_str)
        return absolute_error / value

if __name__ == "__main__":
    import unittest

    class TestSigFigCounter(unittest.TestCase):
        """Test if PrecisionNumber.count_sig_figs() works properly and return the correct number of significant figures."""
        
        def test_no_decmial_point(self):
            """Test numbers that do not contain a decimal point."""
            self.assertEqual(PrecisionNumber.count_sig_figs("120"), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs("205"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("36700"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("21"), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs("9"), 1)
            self.assertEqual(PrecisionNumber.count_sig_figs("1000"), 1)

        def test_with_decimal_point(self):
            """Test numbers that do contain a decimal point."""
            self.assertEqual(PrecisionNumber.count_sig_figs("2.05"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("61.09"), 4)
            self.assertEqual(PrecisionNumber.count_sig_figs("0.500"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("3.000"), 4)
            self.assertEqual(PrecisionNumber.count_sig_figs("80.0000"), 6)
            self.assertEqual(PrecisionNumber.count_sig_figs("70."), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs("0.0025"), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs(".000108"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("0.00040600"), 5)
        
        def test_with_scientific_notation(self):
            """Test numbers that are written in scientific notation (or at least contain an E)."""
            self.assertEqual(PrecisionNumber.count_sig_figs("1.25E+09"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("2.846E-20"), 4)
            self.assertEqual(PrecisionNumber.count_sig_figs("1.002E8"), 4)
            self.assertEqual(PrecisionNumber.count_sig_figs("8.4e2"), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs("71.8E-3"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("1257E0"), 4)
            self.assertEqual(PrecisionNumber.count_sig_figs("0.093e+14"), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs("0.2E2"), 1)
        
        def test_leading_signs(self):
            """Test numbers that contain signs (+ or -) at the start."""
            self.assertEqual(PrecisionNumber.count_sig_figs("+346"), 3)
            self.assertEqual(PrecisionNumber.count_sig_figs("-00017"), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs("-9.180"), 4)
            self.assertEqual(PrecisionNumber.count_sig_figs("+00028000"), 2)
            self.assertEqual(PrecisionNumber.count_sig_figs("-0.028000"), 5)
            self.assertEqual(PrecisionNumber.count_sig_figs("+1.42E-08"), 3)
        
        def test_leading_zeros(self):
            """Test numbers that contain leading zeros."""
            self.assertEqual(PrecisionNumber.count_sig_figs("000012000.0"), 6)
            self.assertEqual(PrecisionNumber.count_sig_figs("0000000100000"), 1)
            self.assertEqual(PrecisionNumber.count_sig_figs("0000.0012070"), 5)

    unittest.main(exit=False)