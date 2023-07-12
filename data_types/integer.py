"""
Integer data type

This module defines integer data type. :code:`UInt` and :code:`SInt` defines generic integer data
type with configurable width. :code:`UInt` and :code:`SInt` provide :code:`to_native` and 
:code:`from_native` method to convert between bit string and native int type by python. 

Other functions provide data type defined by ISA.

TODO: check with softfloat.
"""

from typing_extensions import Self
from .base_type import BaseDataType

class UInt(BaseDataType):
    """
    Generic unsigned integer data type.

    Width is configurable.
    """
    def __init__(self, width: int, value: int = None):
        """
        Construct one data.

        Args:
            width: Width in bit.
            value: Bit string.
        """
        super().__init__(width, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this data.

        Args:
            width: overwrite width of bit string.
        """
        return UInt(width if width else self.width, self.value)

    def to_native(self) -> int:
        """
        Convert to native integer number in Python.
        """
        return self.value

    def from_native(self, value: int) -> Self:
        """
        Convert native integer number in python to UInt.

        Args:
            value: native floating value
        """
        self.value = abs(int(value))
        if value < 0:
            self.value = ((1 << self.width) - self.value)

        return self

    def mul_extend(self, other: BaseDataType) -> Self:
        """
        Multiple two integer and increase width.

        Args:
            other: Another integer value.
        """
        res = self.to_native() * other.to_native()
        width = self.width + other.width

        return UInt(width).from_native(res)


def uint8(value: int = None):
    """
    Generate one 8-bit unsigned integer.

    Args:
        value: Bit string.
    """
    return UInt(8, value)

def uint16(value: int = None):
    """
    Generate one 16-bit unsigned integer.

    Args:
        value: Bit string.
    """
    return UInt(16, value)

def uint32(value: int = None):
    """
    Generate one 32-bit unsigned integer.

    Args:
        value: Bit string.
    """
    return UInt(32, value)

def uint64(value: int = None):
    """
    Generate one 64-bit unsigned integer.

    Args:
        value: Bit string.
    """
    return UInt(64, value)


class SInt(BaseDataType):
    """
    Generic signed integer data type.

    Width is configurable.
    """
    def __init__(self, width: int, value: int = None):
        """
        Construct one data.

        Args:
            width: Width in bit.
            value: Bit string.
        """
        super().__init__(width, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this data.

        Args:
            width: overwrite width of bit string.
        """
        return SInt(width if width else self.width, self.value)

    def to_native(self) -> int:
        """
        Convert to native integer number in Python.
        """
        if self.msb > 0:
            return - ((1 << self.width) - self.value)
        else:
            return self.value

    def from_native(self, value: int) -> Self:
        """
        Convert native integer number in python to UInt.

        Args:
            value: native floating value
        """
        self.value = abs(int(value))
        if value < 0:
            self.value = ((1 << self.width) - self.value)

        return self

    def mul_extend(self, other: BaseDataType) -> Self:
        """
        Multiple two integer and increase width.

        Args:
            other: Another integer value.
        """
        res = self.to_native() * other.to_native()
        width = self.width + other.width

        return SInt(width).from_native(res)


def sint8(value: int = None):
    """
    Generate one 8-bit signed integer.

    Args:
        value: Bit string.
    """
    return SInt(8, value)

def sint16(value: int = None):
    """
    Generate one 16-bit signed integer.

    Args:
        value: Bit string.
    """
    return SInt(16, value)

def sint32(value: int = None):
    """
    Generate one 32-bit signed integer.

    Args:
        value: Bit string.
    """
    return SInt(32, value)

def sint64(value: int = None):
    """
    Generate one 64-bit signed integer.

    Args:
        value: Bit string.
    """
    return SInt(64, value)
