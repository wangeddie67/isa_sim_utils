"""
Integer data type:

- UInt/SInt
- UInt8/UInt16/UInt32/UInt64
- SInt8/SInt16/SInt32/SInt64
"""

from typing_extensions import Self
from .base_type import BaseDataType

class Integer(BaseDataType):
    """
    Integer data type.
    """
    def __init__(self, signed: bool, width: int, value: int = None):
        """
        Construct one data.

        Args:
            signed: Signed or unsigned integer.
            width: Width in bit.
            value: Bit string.
        """
        self._signed = signed

        super().__init__(width, value)

    @property
    def signed(self) -> bool:
        """
        Return whether integer is signed integer or unsigned integer.
        """
        return self._signed

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item

        Args:
            width: overwrite data width.
        """
        return Integer(self.signed, width if width else self.width, self.value)

    def to_native(self) -> int:
        """
        Convert to native integer in Python.
        """
        if self.signed:
            if self.msb > 0:
                return - ((1 << self.width) - self.value)
            else:
                return self.value
        else:
            return self.value

    def from_native(self, value: int) -> Self:
        """
        Convert native integer in python to Integer.
        """
        self.value = abs(int(value))
        if value < 0:
            self.value = ((1 << self.width) - self.value)

        return self

    def mul_extend(self, other: Self) -> Self:
        """
        Multiple two integer and increase width
        """
        res = self.to_native() * other.to_native()
        width = self.width + other.width

        return Integer(self.signed, width).from_native(res)


class UInt(Integer):
    """
    Unsigned integer
    """
    def __init__(self, width: int, value: int = None):
        """
        Construct one data.

        Args:
            signed: Signed or unsigned integer.
            width: Width in bit.
            value: Bit string.
        """
        super().__init__(False, width, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return UInt(width if width else self.width, self.value)

class UInt8(UInt):
    """
    8-bit Unsigned integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(8, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return UInt8(self.value)

class UInt16(UInt):
    """
    16-bit Unsigned integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(16, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return UInt16(self.value)

class UInt32(UInt):
    """
    32-bit Unsigned integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(32, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return UInt32(self.value)

class UInt64(UInt):
    """
    64-bit Unsigned integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(64, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return UInt64(self.value)

class SInt(Integer):
    """
    Signed integer
    """
    def __init__(self, width: int, value: int = None):
        """
        Construct one data.

        Args:
            signed: Signed or unsigned integer.
            width: Width in bit.
            value: Bit string.
        """
        super().__init__(False, width, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return SInt(width if width else self.width, self.value)

class SInt8(SInt):
    """
    8-bit Signed integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(8, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return SInt8(self.value)

class SInt16(SInt):
    """
    16-bit Signed integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(16, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return SInt16(self.value)

class SInt32(SInt):
    """
    32-bit Signed integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(32, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return SInt32(self.value)

class SInt64(SInt):
    """
    64-bit Signed integer.
    """
    def __init__(self, value: int = None):
        """
        Construct one data.

        Args:
            value: Bit string.
        """
        super().__init__(64, value)

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item
        """
        return SInt64(self.value)
