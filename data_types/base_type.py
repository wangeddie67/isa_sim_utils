"""
Base data type.
"""

from typing import Union, Any
from typing_extensions import Self

class BaseDataType():
    """
    Base data type.
    """
    def __init__(self, width: int, value: Any = None) -> Self:
        """
        Construct one data.

        Args:
            width: Width in bit.
            value: Bit string.
        """
        self._width = width
        self._value = None
        self.from_native(value)

    def __index__(self):
        """
        Return an index of value, which can be convert to hex.
        """
        return self.value & ((1 << self.width) - 1)

    def __str__(self):
        """
        Return an string of value.
        """
        return self.__class__.__name__ + "(" + str(self.to_native())

    def __repr__(self):
        """
        Return an string of value.
        """
        return self.__class__.__name__ + "(" + str(self.to_native())

    @property
    def width(self) -> int:
        """
        Return data width in bit.
        """
        return self._width

    @property
    def value(self) -> int:
        """
        Return data value in a bit string.
        """
        return self._value

    @value.setter
    def value(self, value: int = None):
        """
        Set data value by a bit string.
        """
        self._value = value & ((1 << self._width) - 1)

    def copy(self) -> Self:
        """
        Copy instance of this item
        """
        raise NotImplementedError("Implemented in inherent class.")

    def to_native(self) -> Union[int, float]:
        """
        Convert to native data type in python.
        """
        raise NotImplementedError("Implemented in inherent class.")

    def from_native(self, value: Union[int, float]) -> Self:
        """
        Convert native data type in python to value.
        """
        raise NotImplementedError("Implemented in inherent class.")

    def __getitem__(self, idx: int) -> int:
        """
        Get One bit from bit string.
        """
        return (self.value >> idx) & 0x01

    def __setitem__(self, idx: int, value: int):
        """
        Set one bit to bit string.
        """
        if value & 0x01:
            mask = 1 << idx
            self.value = self.value | mask
        else:
            mask = ((1 << self.width) - 1) - (1 << idx)
            self.value = self.value & mask

    def __getslice__(self, msb: int, lsb: int) -> int:
        """
        Get One bit from bit string.
        """
        if msb < lsb:
            msb_ = lsb
            lsb_ = msb
        else:
            msb_ = msb
            lsb_ = lsb
        width = msb_ - lsb_ + 1

        return (self.value >> lsb_) & ((1 << width) - 1)

    def __setslice__(self, msb: int, lsb: int, field: int):
        """
        Set bit field to bit string.
        """
        if msb < lsb:
            msb_ = lsb
            lsb_ = msb
        else:
            msb_ = msb
            lsb_ = lsb
        width = msb_ - lsb_ + 1
        field_ = field & ((1 << width) - 1)
        self.value = self.value - (self.__getslice__(msb_, lsb_) << lsb)
        self.value |= field_ << lsb_

    @property
    def msb(self) -> int:
        """
        Return MSB.
        """
        return (self.value >> (self.width - 1)) & 0x01

    @msb.setter
    def msb(self, value: int) -> int:
        """
        Set MSB.
        """
        if value == 0:
            mask = (1 << (self.width - 1)) - 1
            self.value = self.value & mask
        else:
            mask = 1 << (self.width - 1)
            self.value = self.value | mask

    def _raise_type_error(self, op, a, b = None):
        """
        raise type error.
        """
        if b:
            msg = f"Type not support: {type(a)} {op} {type(b)}."
        else:
            msg = f"Type not support: {op} {type(a)}"
        raise TypeError(msg)


    def __add__(self, other) -> Self:
        """
        Overloading operator +.
        """
        if isinstance(other, (int, float)):
            res = self.to_native() + other
        elif isinstance(other, BaseDataType):
            res = self.to_native() + other.to_native()
        else:
            self._raise_type_error("+", self, other)

        return self.copy().from_native(res)

    def __iadd__(self, other):
        """
        Overloading operator +=.
        """
        res = self.__add__(other)
        self.value = res.value
        return self

    def __sub__(self, other) -> Self:
        """
        Overloading operator -.
        """
        if isinstance(other, (int, float)):
            res = self.to_native() - other
        elif isinstance(other, BaseDataType):
            res = self.to_native() - other.to_native()
        else:
            self._raise_type_error("-", self, other)

        return self.copy().from_native(res)

    def __isub__(self, other):
        """
        Overloading operator -=.
        """
        res = self.__sub__(other)
        self.value = res.value
        return self

    def __mul__(self, other) -> Self:
        """
        Overloading operator *
        """
        if isinstance(other, (int, float)):
            res = self.to_native() * other
        elif isinstance(other, BaseDataType):
            res = self.to_native() * other.to_native()
        else:
            self._raise_type_error("*", self, other)

        return self.copy().from_native(res)

    def __imul__(self, other):
        """
        Overloading operator *=.
        """
        res = self.__mul__(other)
        self.value = res.value
        return self

    def __truediv__(self, other) -> Self:
        """
        Overloading operator /
        """
        if isinstance(other, (int, float)):
            res = self.to_native() / other
        elif isinstance(other, BaseDataType):
            res = self.to_native() / other.to_native()
        else:
            self._raise_type_error("/", self, other)

        return self.copy().from_native(res)

    def __itruediv__(self, other):
        """
        Overloading operator /=.
        """
        res = self.__truediv__(other)
        self.value = res.value
        return self

    def __floordiv__(self, other) -> Self:
        """
        Overloading operator //
        """
        if isinstance(other, (int, float)):
            res = self.to_native() // other
        elif isinstance(other, BaseDataType):
            res = self.to_native() // other.to_native()
        else:
            self._raise_type_error("//", self, other)

        return self.copy().from_native(res)

    def __ifloordiv__(self, other):
        """
        Overloading operator //=.
        """
        res = self.__floordiv__(other)
        self.value = res.value
        return self

    def __mod__(self, other) -> Self:
        """
        Overloading operator %
        """
        if isinstance(other, int):
            res = self.to_native() % other
        elif isinstance(other, BaseDataType):
            res = self.to_native() % other.to_native()
        else:
            self._raise_type_error("%", self, other)

        return self.copy().from_native(res)

    def __imod__(self, other):
        """
        Overloading operator %=.
        """
        res = self.__mod__(other)
        self.value = res.value
        return self

    def __pow__(self, other) -> Self:
        """
        Overloading operator **
        """
        if isinstance(other, int):
            res = int(self.to_native() ** other)
        elif isinstance(other, BaseDataType):
            res = int(self.to_native() ** other.to_native())
        else:
            self._raise_type_error("**", self, other)

        return self.copy().from_native(res)

    def __ipow__(self, other):
        """
        Overloading operator **=.
        """
        res = self.__pow__(other)
        self.value = res.value
        return self

    def __rshift__(self, other) -> Self:
        """
        Overloading operator >>
        """
        if isinstance(other, int):
            res = self.to_native() >> other
        elif isinstance(other, BaseDataType):
            res = self.to_native() >> other.to_native()
        else:
            self._raise_type_error(">>", self, other)

        return self.copy().from_native(res)

    def __irshift__(self, other):
        """
        Overloading operator >>=.
        """
        res = self.__rshift__(other)
        self.value = res.value
        return self

    def __lshift__(self, other) -> Self:
        """
        Overloading operator <<
        """
        if isinstance(other, int):
            res = self.to_native() << other
        elif isinstance(other, BaseDataType):
            res = self.to_native() << other.to_native()
        else:
            self._raise_type_error("<<", self, other)

        return self.copy().from_native(res)

    def __ilshift__(self, other):
        """
        Overloading operator <<=.
        """
        res = self.__ilshift__(other)
        self.value = res.value
        return self

    def __and__(self, other) -> Self:
        """
        Overloading operator &
        """
        if isinstance(other, int):
            res = self.value & other
        elif isinstance(other, BaseDataType):
            res = self.value & other.value
        else:
            self._raise_type_error("&", self, other)

        return self.copy().from_native(res)

    def __iand__(self, other):
        """
        Overloading operator &=
        """
        res = self.__and__(other)
        self.value = res.value
        return self

    def __or__(self, other) -> Self:
        """
        Overloading operator |
        """
        if isinstance(other, int):
            res = self.value | other
        elif isinstance(other, BaseDataType):
            res = self.value | other.value
        else:
            self._raise_type_error("|", self, other)

        return self.copy().from_native(res)

    def __ior__(self, other):
        """
        Overloading operator |=
        """
        res = self.__or__(other)
        self.value = res.value
        return self

    def __xor__(self, other) -> Self:
        """
        Overloading operator ^
        """
        if isinstance(other, int):
            res = self.value ^ other
        elif isinstance(other, BaseDataType):
            res = self.value ^ other.value
        else:
            self._raise_type_error("^", self, other)

        return self.copy().from_native(res)

    def __ixor__(self, other):
        """
        Overloading operator ^=
        """
        res = self.__xor__(other)
        self.value = res.value
        return self

    def __lt__(self, other) -> bool:
        """
        Overloading operator <
        """
        if isinstance(other, int):
            res = self.to_native() < other
        elif isinstance(other, BaseDataType):
            res = self.to_native() < other.to_native()
        else:
            self._raise_type_error("<", self, other)

        return res

    def __gt__(self, other) -> bool:
        """
        Overloading operator >
        """
        if isinstance(other, int):
            res = self.to_native() > other
        elif isinstance(other, BaseDataType):
            res = self.to_native() > other.to_native()
        else:
            self._raise_type_error(">", self, other)

        return res

    def __le__(self, other) -> bool:
        """
        Overloading operator <=
        """
        if isinstance(other, int):
            res = self.to_native() <= other
        elif isinstance(other, BaseDataType):
            res = self.to_native() <= other.to_native()
        else:
            self._raise_type_error("<=", self, other)

        return res

    def __ge__(self, other) -> bool:
        """
        Overloading operator >=
        """
        if isinstance(other, int):
            res = self.to_native() >= other
        elif isinstance(other, BaseDataType):
            res = self.to_native() >= other.to_native()
        else:
            self._raise_type_error(">=", self, other)

        return res

    def __eq__(self, other) -> bool:
        """
        Overloading operator ==
        """
        if isinstance(other, int):
            res = self.to_native() == other
        elif isinstance(other, BaseDataType):
            res = self.to_native() == other.to_native()
        else:
            self._raise_type_error("==", self, other)

        return res

    def __ne__(self, other) -> bool:
        """
        Overloading operator !=
        """
        if isinstance(other, int):
            res = self.to_native() != other
        elif isinstance(other, BaseDataType):
            res = self.to_native() != other.to_native()
        else:
            self._raise_type_error("!=", self, other)

        return res

    def __neg__(self) -> Self:
        """
        Overloading unary operator -
        """
        res = - self.to_native()
        return self.copy().from_native(res)

    def __pos__(self) -> Self:
        """
        Overloading unary operator +
        """
        return self.copy()

    def __invert__(self) -> Self:
        """
        Overloading unary operator ~
        """
        res = ((1 << self.width) - 1) - self.value
        return self.copy().from_native(res)
