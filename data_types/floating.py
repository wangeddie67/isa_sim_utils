"""
Unsigned Integer data type:

- Floating
- Float8/Float16/BFloat/HFloat/SFloat/DFloat
"""

from typing_extensions import Self
import math
from .base_type import BaseDataType

class Floating(BaseDataType):
    """
    Floating data type.
    """
    def __init__(self, exp_width: bool, man_width: int, value: int = None):
        """
        Construct one data.

        Args:
            signed: Signed or unsigned integer.
            width: Width in bit.
            value: Bit string.
        """
        self._exp_width = exp_width
        self._man_width = man_width

        super().__init__(1 + exp_width + man_width, value)

    @property
    def bias(self) -> int:
        """
        Return bias of exponent.
        """
        return (1 << (self._exp_width - 1)) - 1

    @property
    def exponent(self) -> int:
        """
        Return whether integer is signed integer or unsigned integer.
        """
        exp_lsb = self._man_width
        exp_msb = self._man_width + self._exp_width - 1

        return self.__getslice__(exp_msb, exp_lsb) - self.bias

    @property
    def mantissa(self) -> float:
        """
        Return whether integer is signed integer or unsigned integer.
        """
        man_lsb = 0
        man_msb = self._man_width - 1
        return self.__getslice__(man_msb, man_lsb) / (2 ** self._man_width)

    @property
    def signature(self) -> float:
        """
        Return signature bit.
        """
        return self.msb

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        return Floating(self._exp_width, self._man_width, self.value)

    def to_native(self) -> float:
        """
        Convert to native integer in Python.
        """
        signature = -1 if self.signature else 1
        exponent = self.exponent
        mantissa = self.mantissa
        return signature * (2 ** exponent) * (1 + mantissa)

    def from_native(self, value: float) -> Self:
        """
        Convert native integer in python to Integer.
        """
        math_man, math_exp = math.frexp(float(value))

        signature = 1 if math_man < 0 else 0
        mantissa = int((abs(math_man) * 2 - 1) * (2 ** self._man_width))
        exponent = math_exp - 1 + self.bias
        if exponent < 0:
            exponent = 0
        if exponent >= (1 << self._exp_width):
            exponent = (1 << self._exp_width) - 1

        self.value = 0
        self.msb = signature

        exp_lsb = self._man_width
        exp_msb = self._man_width + self._exp_width - 1
        self.__setslice__(exp_msb, exp_lsb, exponent)

        man_lsb = 0
        man_msb = self._man_width - 1
        self.__setslice__(man_lsb, man_msb, mantissa)

        return self


class FP8E4M3(Floating):
    """
    FP8 floating-point number.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(4, 3, value)

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        return FP8E4M3(self.value)

class FP8E5M2(Floating):
    """
    FP8 floating-point number.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(5, 2, value)

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        return FP8E5M2(self.value)

class Float16(Floating):
    """
    FP16 floating-point number.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(8, 7, value)

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        return Float16(self.value)

class HpFloat(Floating):
    """
    Half-precision floating-point number.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(5, 10, value)

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        return HpFloat(self.value)

class SpFloat(Floating):
    """
    Single-precision floating-point number.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(8, 23, value)

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        return SpFloat(self.value)

class DpFloat(Floating):
    """
    Double-precision floating-point number.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(11, 52, value)

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        return DpFloat(self.value)
