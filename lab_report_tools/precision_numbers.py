import math

def get_leading_place_value(value: float|int) -> int:
    """Get the place value of the leading digit of the input number."""
    return math.floor(math.log(abs(value), 10))
    
def string_to_sig_figs(value: float|int, sig_figs: int) -> str:
    """Return the string representation of the input value rounded to the desired number of significant figures."""
    return f"{value:#.{sig_figs}G}"

def round_to_sig_figs(value: float|int, sig_figs: int) -> float:
    """Round the input value to the desired number of significant figures."""
    return float(string_to_sig_figs(value, sig_figs))


class PrecisionNumber:
    """This class is used to create numbers that also have the number of sig figs and the absolute error attached to them and propogated through operations.
    Operations with normal float|int numbers will interpret them as being exact numbers.
    """

    def __init__(self, value_str: str|float|int, *, sig_figs: int = None, decimal_place: int = None, absolute_error: float|int = None, relative_error: float|int = None, default_style: str = "sig_figs") -> None:
        """Initialize a PrecisionNumber with the input *value_str*.
        If *sig_figs* and *decimal_place* are both not set, then they will be inferred automatically. If one is set, that value will be used to deterine both. If both are set, then an error will be raised.
        If *absolute_error* and *relative_error* are both not set, then they will be inferred automatically. If one is set, that value will be used to deterine both. If both are set, then an error will be raised.
        """
        if not isinstance(value_str, (str, float, int)):
            raise TypeError("PrecisionNumber *value_str* argument must be of type str|float|int")
        self._value = float(value_str)
        self._leading_place_value = get_leading_place_value(self.value)
        self.default_style = default_style

        if sig_figs == None and decimal_place == None:
            self.sig_figs = self.get_sig_figs(str(value_str))
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
    
    def __repr__(self) -> str:
        """Method to return a string representing the PrecisionNumber object instance."""
        return f"PrecisionNumber({self.value}, sig_figs={self.sig_figs}, absolute_error={self.absolute_error}{'' if self.default_style == 'sig_figs' else ', default_style=' + repr(self.default_style)})"
    
    def __str__(self) -> str:
        """Method to return a nice string representation of the PrecisionNumber object instance.
        *default_style* is passed to the *formatted* method to generate the str.
        """
        return self.formatted(self.default_style)

    def formatted(self, style: str) -> str:
        """Return a string representation of the number according to the input style."""
        if style == "sig_figs":
            return string_to_sig_figs(self.value, self.sig_figs)
        elif style == "absolute_error":
            abs_err_rounded = round_to_sig_figs(self.absolute_error, 1)
            abs_err_pv = get_leading_place_value(abs_err_rounded)
            rounded_value_str = string_to_sig_figs(self.value, 1+(get_leading_place_value(round(self.value, -abs_err_pv)))-abs_err_pv)
            if "E" in rounded_value_str:
                num_part, power_part = rounded_value_str.split("E")
                power_part_value = int(power_part)
                decimalized_abs_err = f"{abs_err_rounded / 10**power_part_value:.{-abs_err_pv + power_part_value}f}"
                return f"({num_part} ± {decimalized_abs_err})E{power_part}"
            else:
                return f"{rounded_value_str} ± {abs_err_rounded:.{-abs_err_pv}f}"
        elif style == "relative_error":
            percent_err_str = string_to_sig_figs(self.relative_error * 100, 3) + "%"
            abs_err_rounded = round_to_sig_figs(self.absolute_error, 1)
            abs_err_pv = get_leading_place_value(abs_err_rounded)
            rounded_value_str = string_to_sig_figs(self.value, 1+(get_leading_place_value(round(self.value, -abs_err_pv)))-abs_err_pv)
            return f"{rounded_value_str} ± {percent_err_str}"
        else:
            return repr(self)

    def copy(self) -> 'PrecisionNumber':
        """Return a copy of the number."""
        return PrecisionNumber(self.value, sig_figs=self.sig_figs, absolute_error=self.absolute_error, default_style=self.default_style)


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
        self._relative_error = value / abs(self._value)
    
    @property
    def relative_error(self) -> float:
        """Get the relative error of the number."""
        return self._relative_error
    @relative_error.setter
    def relative_error(self, value: float|int):
        """Set the relative error to the input value, and update the absolute error accordingly."""
        value = float(value)
        self._relative_error = value
        self._absolute_error = value * abs(self._value)


    def __eq__(self, other: 'PrecisionNumber') -> bool:
        """Two numbers are equal if they have the same value, number of sig figs, and absolute error."""
        if isinstance(other, PrecisionNumber):
            return math.isclose(self.value, other.value) and\
                math.isclose(self.sig_figs, other.sig_figs) and\
                math.isclose(self.absolute_error, other.absolute_error)
        else:
            return NotImplemented

    def __ne__(self, other: 'PrecisionNumber') -> bool:
        """Two numbers are not equal if they do not have the same value, number of sig figs, and absolute error."""
        return not (self == other)

    def __lt__(self, other: 'PrecisionNumber') -> bool:
        """The values of the numbers should be compared as expected."""
        if isinstance(other, PrecisionNumber):
            return self.value < other.value
        else:
            return NotImplemented

    def __le__(self, other: 'PrecisionNumber') -> bool:
        """The values of the numbers should be compared as expected."""
        if isinstance(other, PrecisionNumber):
            return self.value <= other.value
        else:
            return NotImplemented

    def __gt__(self, other: 'PrecisionNumber') -> bool:
        """The values of the numbers should be compared as expected."""
        if isinstance(other, PrecisionNumber):
            return self.value > other.value
        else:
            return NotImplemented

    def __ge__(self, other: 'PrecisionNumber') -> bool:
        """The values of the numbers should be compared as expected."""
        if isinstance(other, PrecisionNumber):
            return self.value >= other.value
        else:
            return NotImplemented


    def __pos__(self) -> 'PrecisionNumber':
        """The positive of a number is just that number."""
        return self * 1
    
    def __neg__(self) -> 'PrecisionNumber':
        """The negative of a number is just that number with its value multipiled by negative one."""
        return self * -1
    
    def __abs__(self) -> 'PrecisionNumber':
        """The absolute value of a number just that number with its value made positive."""
        return PrecisionNumber(abs(self.value), sig_figs=self.sig_figs, absolute_error=self.absolute_error)
    
    def __float__(self) -> float:
        return float(self.value)
    
    def __int__(self) -> int:
        return int(self.value)


    def __add__(self, other: 'PrecisionNumber|float|int', /) -> 'PrecisionNumber':
        """When two numbers are added together, the higher decimal place is used in the result and the absolute errors add together."""
        if isinstance(other, PrecisionNumber):
            sum = self.value + other.value
            decimal_place = max(self.decimal_place, other.decimal_place)
            absolute_error = self.absolute_error + other.absolute_error
        elif isinstance(other, (float, int)):
            sum = self.value + other
            decimal_place = self.decimal_place
            absolute_error = self.absolute_error
        else:
            return NotImplemented
        if sum == 0:
            return 0
        return PrecisionNumber(sum, decimal_place=decimal_place, absolute_error=absolute_error)

    def __radd__(self, other: 'float|int', /) -> 'PrecisionNumber':
        """When two numbers are added together, the higher decimal place is used in the result and the absolute errors add together."""
        return self + other

    def __mul__(self, other: 'PrecisionNumber|float|int', /) -> 'PrecisionNumber':
        """When two numbers are multiplied together, the lower number of sig figs is used in the result and the relative errors add together."""
        if isinstance(other, PrecisionNumber):
            product = self.value * other.value
            sig_figs = min(self.sig_figs, other.sig_figs)
            relative_error = self.relative_error + other.relative_error
        elif isinstance(other, (float, int)):
            product = self.value * other
            sig_figs = self.sig_figs
            relative_error = self.relative_error
        else:
            return NotImplemented
        if product == 0:
            return 0
        return PrecisionNumber(product, sig_figs=sig_figs, relative_error=relative_error)

    def __rmul__(self, other: 'float|int', /) -> 'PrecisionNumber':
        """When two numbers are multiplied together, the lower number of sig figs is used in the result and the relative errors add together."""
        return self * other

    def __sub__(self, other: 'PrecisionNumber|float|int', /) -> 'PrecisionNumber':
        """When two numbers are subtracted, the higher decimal place is used in the result and the absolute errors add together."""
        return self + (-1 * other)

    def __rsub__(self, other: 'float|int', /) -> 'PrecisionNumber':
        """When two numbers are subtracted, the higher decimal place is used in the result and the absolute errors add together."""
        return (-1 * self) + other
    
    def __truediv__(self, other: 'PrecisionNumber|float|int', /) -> 'PrecisionNumber':
        """When two numbers are divided, the lower number of sig figs is used in the result and the relative errors add together."""
        if isinstance(other, PrecisionNumber):
            quotient = self.value / other.value
            sig_figs = min(self.sig_figs, other.sig_figs)
            relative_error = self.relative_error + other.relative_error
        elif isinstance(other, (float, int)):
            quotient = self.value / other
            sig_figs = self.sig_figs
            relative_error = self.relative_error
        else:
            return NotImplemented
        if quotient == 0:
            return 0
        return PrecisionNumber(quotient, sig_figs=sig_figs, relative_error=relative_error)
    
    def __rtruediv__(self, other: 'float|int', /) -> 'PrecisionNumber':
        """When two numbers are divided, the lower number of sig figs is used in the result and the relative errors add together."""
        if isinstance(other, (float, int)):
            quotient = other / self.value
            sig_figs = self.sig_figs
            relative_error = self.relative_error
            if quotient == 0:
                return 0
            return PrecisionNumber(quotient, sig_figs=sig_figs, relative_error=relative_error)
        else:
            return NotImplemented
    
    def __pow__(self, other: 'float|int', /) -> 'PrecisionNumber':
        """When a number is raised to an exact power, the uncertainty propogates as if it were repeated multiplication."""
        if isinstance(other, (float, int)):
            power = self.value ** other
            sig_figs = self.sig_figs
            relative_error = abs(self.relative_error * other)
            return PrecisionNumber(power, sig_figs=sig_figs, relative_error=relative_error)
        else:
            return NotImplemented


    @staticmethod
    def get_sig_figs(value_str: str) -> int:
        """Count the number of significant figures (sig figs) in the input number string."""
        value = float(value_str)
        value_str = value_str.strip().upper()
        value_str = value_str.replace("_", "")
        value_str = value_str.replace("+", "")
        value_str = value_str.replace("-", "")
        if "E" in value_str:
            num_part = value_str.split("E")[0]
            return PrecisionNumber.get_sig_figs(num_part)
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
        leading_place_value = get_leading_place_value(value)
        sf_count = PrecisionNumber.get_sig_figs(value_str)
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
        """Test if PrecisionNumber.get_sig_figs() works properly and return the correct number of significant figures."""
        
        def test_no_decmial_point(self):
            """Test numbers that do not contain a decimal point."""
            self.assertEqual(PrecisionNumber.get_sig_figs("120"), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs("205"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("36700"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("21"), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs("9"), 1)
            self.assertEqual(PrecisionNumber.get_sig_figs("1000"), 1)

        def test_with_decimal_point(self):
            """Test numbers that do contain a decimal point."""
            self.assertEqual(PrecisionNumber.get_sig_figs("2.05"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("61.09"), 4)
            self.assertEqual(PrecisionNumber.get_sig_figs("0.500"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("3.000"), 4)
            self.assertEqual(PrecisionNumber.get_sig_figs("80.0000"), 6)
            self.assertEqual(PrecisionNumber.get_sig_figs("70."), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs("0.0025"), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs(".000108"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("0.00040600"), 5)

        def test_with_scientific_notation(self):
            """Test numbers that are written in scientific notation (or at least contain an E)."""
            self.assertEqual(PrecisionNumber.get_sig_figs("1.25E+09"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("2.846E-20"), 4)
            self.assertEqual(PrecisionNumber.get_sig_figs("1.002E8"), 4)
            self.assertEqual(PrecisionNumber.get_sig_figs("8.4e2"), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs("71.8E-3"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("1257E0"), 4)
            self.assertEqual(PrecisionNumber.get_sig_figs("0.093e+14"), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs("0.2E2"), 1)

        def test_leading_signs(self):
            """Test numbers that contain signs (+ or -) at the start."""
            self.assertEqual(PrecisionNumber.get_sig_figs("+346"), 3)
            self.assertEqual(PrecisionNumber.get_sig_figs("-00017"), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs("-9.180"), 4)
            self.assertEqual(PrecisionNumber.get_sig_figs("+00028000"), 2)
            self.assertEqual(PrecisionNumber.get_sig_figs("-0.028000"), 5)
            self.assertEqual(PrecisionNumber.get_sig_figs("+1.42E-08"), 3)

        def test_leading_zeros(self):
            """Test numbers that contain leading zeros."""
            self.assertEqual(PrecisionNumber.get_sig_figs("000012000.0"), 6)
            self.assertEqual(PrecisionNumber.get_sig_figs("0000000100000"), 1)
            self.assertEqual(PrecisionNumber.get_sig_figs("0000.0012070"), 5)

    class TestOperations(unittest.TestCase):
        """Test if the operations with PrecisionNumber objects work properly."""
        def test_equality(self):
            """Test if the equality operator (==) works properly."""
            self.assertEqual(PrecisionNumber(0.1, sig_figs=3, absolute_error=0.001) + PrecisionNumber(0.2, sig_figs=3, absolute_error=0.001), 
                PrecisionNumber(0.3, decimal_place=-3, absolute_error=0.002))

        def test_addition(self):
            """Test if addition (+) works properly."""
            self.assertEqual(PrecisionNumber("65.0") + PrecisionNumber("0.05") + PrecisionNumber("179.1"),
                PrecisionNumber("244.15", decimal_place=-1 ,absolute_error=0.21))
            self.assertEqual(273.15 + PrecisionNumber("24.1"),
                PrecisionNumber(297.25, decimal_place=-1, absolute_error=0.1))
            self.assertEqual(+PrecisionNumber("24"), 
                PrecisionNumber("24"))
        
        def test_subtraction(self):
            """Test if subtraction (-) works properly."""
            self.assertEqual(PrecisionNumber("175") - PrecisionNumber("22.5"),
                PrecisionNumber(152.5, decimal_place=0, absolute_error=1.1))
            self.assertEqual(100 - PrecisionNumber("63.2"),
                PrecisionNumber(36.8, sig_figs=3, absolute_error=0.1))
            self.assertEqual(-PrecisionNumber("24"), 
                PrecisionNumber("-24"))
        
        def test_multiplication(self):
            """Test if multiplication (*) works properly."""
            self.assertEqual(PrecisionNumber("17") * PrecisionNumber("1.08"),
                PrecisionNumber(18.36, sig_figs=2, relative_error=(1/17 + 0.01/1.08)))
            self.assertEqual(PrecisionNumber("23.0") * PrecisionNumber("2"),
                PrecisionNumber(46, sig_figs=1, relative_error=(0.1/23 + 1/2)))
        
        def test_division(self):
            """Test if division (/) works properly."""
            self.assertEqual(PrecisionNumber("3.23E-23") / PrecisionNumber("2.1E-10"),
                PrecisionNumber(1.538095238095238e-13, sig_figs=2, absolute_error=7.800453514739228e-15))
            self.assertEqual(1 / PrecisionNumber("2"),
                PrecisionNumber(0.5, sig_figs=1, relative_error=0.5))

        def test_exponentiation(self):
            """Test if raising an uncertain number to an exact power (**) works properly."""
            self.assertEqual(PrecisionNumber("2")**-1,
                PrecisionNumber(0.5, sig_figs=1, relative_error=0.5))
            self.assertEqual(PrecisionNumber("15.5")**3,
                PrecisionNumber(3_723.875, sig_figs=3, absolute_error=72.075))
            self.assertEqual(PrecisionNumber("64")**0.5,
                PrecisionNumber(8, sig_figs=2, relative_error=0.0078125))


    unittest.main(exit=False)