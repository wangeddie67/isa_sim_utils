"""
Base data type.
"""

from typing import Union, Any
from typing_extensions import Self

def _is_x(data) -> bool:
    """
    Return true if the data is X.
    """
    return isinstance(data, BaseDataType) and data.value is None

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
        if value is not None:
            self.from_native(value)

    def _is_x(self) -> bool:
        """
        Return true if the data is X.
        """
        return self.value is None

    def __index__(self):
        """
        Return an index of value, which can be convert to hex.
        """
        if self._is_x():
            return 0
        else:
            return self.value & ((1 << self.width) - 1)

    def __str__(self):
        """
        Return an string of value.
        """
        if self._is_x():
            return ""
        else:
            return hex(self)

    def __repr__(self):
        """
        Return an string of value.
        """
        if self._is_x():
            return self.__class__.__name__ + "(" + str(None) + ")"
        else:
            return self.__class__.__name__ + "(" + str(self.to_native()) + ")"

    def _raise_type_error(self, op, a, b = None):
        """
        raise type error.
        """
        if b:
            msg = f"Type not support: {type(a)} {op} {type(b)}."
        else:
            msg = f"Type not support: {op} {type(a)}"
        raise TypeError(msg)

    def _raise_value_error(self):
        """
        raise value error.
        """
        raise ValueError("Cannot operate on X value.")

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

    def set_x_value(self):
        """
        Set data value to x.
        """
        self._value = None

    def copy(self, width=None) -> Self:
        """
        Copy instance of this item.

        Args:
            width: overwrite data width.
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

    def __getitem__(self, idx: int) -> Self:
        """
        Get One bit from bit string.
        """
        if isinstance(idx, slice):
            if idx.start < idx.stop:
                msb_ = idx.stop
                lsb_ = idx.start
            else:
                msb_ = idx.start
                lsb_ = idx.stop
            width = msb_ - lsb_ + 1
        elif isinstance(idx, tuple):
            if idx[0] < idx[1]:
                msb_ = idx[1]
                lsb_ = idx[0]
            else:
                msb_ = idx[0]
                lsb_ = idx[1]
            width = msb_ - lsb_ + 1
        else:
            msb_ = idx
            lsb_ = idx
            width = 1

        if self._is_x():
            return self.copy(width)
        else:
            res = self.copy(width)
            res.value = (self.value >> lsb_) & ((1 << width) - 1)
            return res

    def __setitem__(self, idx: int, value: int):
        """
        Set one bit to bit string.
        """
        # If value is None, ignore operation.
        if value is None:
            return

        if isinstance(idx, slice):
            if idx.start < idx.stop:
                msb_ = idx.stop
                lsb_ = idx.start
            else:
                msb_ = idx.start
                lsb_ = idx.stop
            width = msb_ - lsb_ + 1
        elif isinstance(idx, tuple):
            if idx[0] < idx[1]:
                msb_ = idx[1]
                lsb_ = idx[0]
            else:
                msb_ = idx[0]
                lsb_ = idx[1]
            width = msb_ - lsb_ + 1
        else:
            msb_ = idx
            lsb_ = idx
            width = 1

        if self._is_x():
            self.value = 0

        field_ = value & ((1 << width) - 1)
        old_value = (self.value >> lsb_) & ((1 << width) - 1)
        self.value = self.value - (old_value << lsb_)
        self.value |= field_ << lsb_

    @property
    def msb(self) -> int:
        """
        Return MSB.
        """
        if self._is_x():
            self._raise_value_error()
        else:
            return (self.value >> (self.width - 1)) & 0x01

    @msb.setter
    def msb(self, value: int) -> int:
        """
        Set MSB.
        """
        if self._is_x():
            self.value = 0

        if value == 0:
            mask = (1 << (self.width - 1)) - 1
            self.value = self.value & mask
        else:
            mask = 1 << (self.width - 1)
            self.value = self.value | mask


    def __add__(self, other) -> Self:
        """
        Overloading operator +.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            return self.copy().set_x_value()

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
        if self._is_x() or _is_x(other):
            self._raise_value_error()

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
        if self._is_x() or _is_x(other):
            self._raise_value_error()

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
        if self._is_x() or _is_x(other):
            self._raise_value_error()

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
        if self._is_x() or _is_x(other):
            self._raise_value_error()

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
        if self._is_x() or _is_x(other):
            self._raise_value_error()

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
        if self._is_x() or _is_x(other):
            self._raise_value_error()

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
        if self._is_x():
            return self.copy().set_x_value()

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
        if self._is_x():
            return self.copy().set_x_value()

        res = ((1 << self.width) - 1) - self.value
        return self.copy().from_native(res)
