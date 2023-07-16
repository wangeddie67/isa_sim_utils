"""
Floating-point data type

This module defines floating-point data type. :code:`Floating` defines generic floating-point data
type with configurable width of exponent and mantissa. :code:`Floating` provides :code:`to_native`
and :code:`from_native` method to convert between bit string and native float type by python.

Other functions provide data type defined by ISA.

================= ======== ========
Type              Exponent Mantissa
================= ======== ========
FP8 (E4M3)        4        3
FP8 (E5M2)        5        2
FP16              8        7
Half-precision    5        10
Single-precision  8        23
Double-precision  11       52
================= ======== ========

Mantissa does not include integer part.

TODO: check with softfloat.
"""

from typing_extensions import Self
import math
from .base_type import BaseDataType

class Floating(BaseDataType):
    """
    Generic floating data type.

    Width of exponent field and mantissa field is configurable.

    Attributes:
        _exp_width: With of exponent field.
        _man_width: With of mantissa field.
    """
    def __init__(self, exp_width: bool, man_width: int, value: int = None):
        """
        Construct one data.

        Args:
            exp_width: bit width of exponent field.
            man_width: bit width of mantissa field. (Except integer part)
            value: Bit string.
        """
        self._exp_width = exp_width
        self._man_width = man_width

        super().__init__(1 + exp_width + man_width, value)

    @property
    def bias(self) -> int:
        """
        Return exponent bias.
        """
        return (1 << (self._exp_width - 1)) - 1

    @property
    def exponent(self) -> int:
        """
        Return exponent after bias.
        """
        exp_lsb = self._man_width
        exp_msb = self._man_width + self._exp_width - 1

        return self.__getslice__(exp_msb, exp_lsb) - self.bias

    @property
    def mantissa(self) -> float:
        """
        Return mantissa after scaling to fraction, without integer part.
        """
        man_lsb = 0
        man_msb = self._man_width - 1
        return self.__getslice__(man_msb, man_lsb) / (2 ** self._man_width)

    @property
    def signature(self) -> int:
        """
        Return signature bit. True means negative.
        """
        return self.msb

    def copy(self) -> Self:
        """
        Copy instance of this data.
        """
        return Floating(self._exp_width, self._man_width, self.value)

    def to_native(self) -> float:
        """
        Convert to native floating-point number in Python.
        """
        signature = -1 if self.signature else 1
        exponent = self.exponent
        mantissa = self.mantissa
        return signature * (2 ** exponent) * (1 + mantissa)

    def from_native(self, value: float) -> Self:
        """
        Convert native floating-point number in python to Floating.

        Args:
            value: native floating value
        """
        # Get exponent and mantissa by math library.
        # math_man in range [0.5 1)
        math_man, math_exp = math.frexp(float(value))

        signature = 1 if math_man < 0 else 0
        mantissa = int((abs(math_man) * 2 - 1) * (2 ** self._man_width))
        exponent = math_exp - 1 + self.bias

        # Saturating exponent.
        if exponent < 0:
            exponent = 0
        if exponent >= (1 << self._exp_width):
            exponent = (1 << self._exp_width) - 1

        # Construct bit string.
        self.value = 0
        self.msb = signature

        exp_lsb = self._man_width
        exp_msb = self._man_width + self._exp_width - 1
        self.__setslice__(exp_msb, exp_lsb, exponent)

        man_lsb = 0
        man_msb = self._man_width - 1
        self.__setslice__(man_lsb, man_msb, mantissa)

        return self


def fp8_e4m3(value: int = None):
    """
    Generate one FP8 (E4M3) floating-point number.

    Args:
        value: Bit string.
    """
    return Floating(5, 2, value)

def fp8_e5m2(value: int = None):
    """
    Generate one FP8 (E5M2) floating-point number.

    Args:
        value: Bit string.
    """
    return Floating(5, 2, value)

def float16(value: int = None):
    """
    Generate one FP16 floating-point number.

    Args:
        value: Bit string.
    """
    return Floating(8, 7, value)

def hpfloat(value: int = None):
    """
    Generate one half-precision floating-point number.

    Args:
        value: Bit string.
    """
    return Floating(5, 10, value)

def spfloat(value: int = None):
    """
    Generate one single-precision floating-point number.

    Args:
        value: Bit string.
    """
    return Floating(8, 23, value)

def dpfloat(value: int = None):
    """
    Generate one double-precision floating-point number.

    Args:
        value: Bit string.
    """
    return Floating(11, 52, value)
