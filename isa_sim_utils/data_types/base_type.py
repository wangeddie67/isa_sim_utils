"""
Generic data type.

This module defines generic data type with configurable width :code:`BaseDataType`. The value is 
stored in :code:`BaseDataType._value` as bit string. :code:`to_native` and :code:`from_native` 
convert bit string with python native data type.

:code:`BaseDataType` cannot be used directly. Before employed, it must be inherited with following
functions overloaded:

- :code:`to_native`: Convert bit string to python native data type.
- :code:`from_native`: Covert python native data type to bit string.
- :code:`copy`: Return a copied instance with the same type.

:code:`BaseDataType` overloading all operators defined by python as follow:

================= ===================== =========== ==========
Operator          Function              Return type X state
================= ===================== =========== ==========
:code:`x[a]`      :code:`__getitem__`   Self ^2     X
:code:`x[a,b]`    :code:`__getitem__`   Self ^2     X
:code:`x[a]=`     :code:`__setitem__`               ^1
:code:`x[a,b]=`   :code:`__setitem__`               ^1
:code:`a + b`     :code:`__add__`       Self        X
:code:`a += b`    :code:`__iadd__`                  X
:code:`a - b`     :code:`__sub__`       Self        X
:code:`a -= b`    :code:`__isub__`                  X
:code:`a * b`     :code:`__mul__`       Self        X
:code:`a *= b`    :code:`__imul__`                  X
:code:`a / b`     :code:`__truediv__`   Self        X
:code:`a /= b`    :code:`__itruediv__`              X
:code:`a // b`    :code:`__floordiv__`  Self        X
:code:`a //= b`   :code:`__ifloordiv__`             X
:code:`a % b`     :code:`__mod__`       Self        X
:code:`a %= b`    :code:`__imod__`                  X
:code:`a ** b`    :code:`__pow__`       Self        X
:code:`a **= b`   :code:`__ipow__`                  X
:code:`a >> b`    :code:`__rshift__`    Self        X
:code:`a >>= b`   :code:`__irshift__`               X
:code:`a << b`    :code:`__lshift__`    Self        X
:code:`a <<= b`   :code:`__ilshift__`               X
:code:`a & b`     :code:`__and__`       Self        X
:code:`a &= b`    :code:`__iand__`                  X
:code:`a | b`     :code:`__or__`        Self        X
:code:`a |= b`    :code:`__ior__`                   X
:code:`a ^ b`     :code:`__xor__`       Self        X
:code:`a ^= b`    :code:`__ixor__`                  X
:code:`a < b`     :code:`__lt__`        boolean     ValueError
:code:`a > b`     :code:`__gt__`        boolean     ValueError
:code:`a <= b`    :code:`__le__`        boolean     ValueError
:code:`a >= b`    :code:`__ge__`        boolean     ValueError
:code:`a == b`    :code:`__eq__`        boolean     ValueError
:code:`a != b`    :code:`__ne__`        boolean     ValueError
:code:`-x`        :code:`__neg__`       Self        X
:code:`+x`        :code:`__pos__`       Self        X
:code:`~x`        :code:`__invert__`    Self        X
:code:`bool(x)`   :code:`__bool__`      boolean     ValueError
================= ===================== =========== ==========

- Note 1: if field value is X, skip operation. If field value is not X but :code:`self._value` is X, 
  set field and set other bits to zero.
- Note 2: return type Self means that return the same type as inherited data type.

Operator can raise two kind of exception:

- If either operand is not :code:`int`, :code:`float` or :code:`BaseDataType`, raise TypeError.
- If operators cannot perform on X state, raise ValueError.
  - Operators that return boolean value cannot operate on X state.
"""

from typing import Union, Any
from typing_extensions import Self
from .mask_base import MaskBase

def _is_x(data) -> bool:
    """
    Return true if the data is X.
    """
    return isinstance(data, BaseDataType) and data.value is None

class BaseDataType():
    """
    Base bit-string data type.

    This class defines a generic bit-string data type with configurable width.

    Attributes:
        _width: width of bit-string.
        _value: value of bit-string.
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

    def __index__(self) -> int:
        """
        Return an index of value, which is used by :code:`hex()` or :code:`oct()`.
        """
        if self._is_x():
            return 0
        else:
            return self.value & ((1 << self.width) - 1)

    def __str__(self) -> str:
        """
        Return an string of value. Return empty string if the value is x.
        """
        if self._is_x():
            return ""
        else:
            return hex(self)

    def __repr__(self) -> str:
        """
        Return an string of type and value.
        """
        if self._is_x():
            return self.__class__.__name__ + "(" + str(None) + ")"
        else:
            return self.__class__.__name__ + "(" + str(self.to_native()) + ")"

    def _raise_type_error(self, op: str, a: Self, b: Self = None):
        """
        Raise type error if operation cannot perform on operand a and b.

        Args:
            - op: Operation in string.
            - a: Operand A.
            - b: Operand B.
        """
        if b:
            msg = f"Type not support: {type(a)} {op} {type(b)}."
        else:
            msg = f"Type not support: {op} {type(a)}"
        raise TypeError(msg)

    def _raise_value_error(self, op: str):
        """
        Raise X value error if operand cannot perform on X value..
        """
        msg = f"Value not support: {op} cannot operate on X value."
        raise ValueError(msg)

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

    def set_x(self):
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
            self._raise_value_error("msb")
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
        Overloading operator :code:`+`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, (int, float)):
            res = self.to_native() + other
        elif isinstance(other, BaseDataType):
            res = self.to_native() + other.to_native()
        else:
            self._raise_type_error("+", self, other)

        return self.copy().from_native(res)

    def __iadd__(self, other):
        """
        Overloading operator :code:`+=`.
        """
        res = self.__add__(other)
        self.value = res.value
        return self

    def __sub__(self, other) -> Self:
        """
        Overloading operator :code:`-`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, (int, float)):
            res = self.to_native() - other
        elif isinstance(other, BaseDataType):
            res = self.to_native() - other.to_native()
        else:
            self._raise_type_error("-", self, other)

        return self.copy().from_native(res)

    def __isub__(self, other):
        """
        Overloading operator :code:`-=`.
        """
        res = self.__sub__(other)
        self.value = res.value
        return self

    def __mul__(self, other) -> Self:
        """
        Overloading operator :code:`*`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, (int, float)):
            res = self.to_native() * other
        elif isinstance(other, BaseDataType):
            res = self.to_native() * other.to_native()
        else:
            self._raise_type_error("*", self, other)

        return self.copy().from_native(res)

    def __imul__(self, other):
        """
        Overloading operator :code:`*=`.
        """
        res = self.__mul__(other)
        self.value = res.value
        return self

    def __truediv__(self, other) -> Self:
        """
        Overloading operator :code:`/`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, (int, float)):
            res = self.to_native() / other
        elif isinstance(other, BaseDataType):
            res = self.to_native() / other.to_native()
        else:
            self._raise_type_error("/", self, other)

        return self.copy().from_native(res)

    def __itruediv__(self, other):
        """
        Overloading operator :code:`/=`.
        """
        res = self.__truediv__(other)
        self.value = res.value
        return self

    def __floordiv__(self, other) -> Self:
        """
        Overloading operator :code:`//`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, (int, float)):
            res = self.to_native() // other
        elif isinstance(other, BaseDataType):
            res = self.to_native() // other.to_native()
        else:
            self._raise_type_error("//", self, other)

        return self.copy().from_native(res)

    def __ifloordiv__(self, other):
        """
        Overloading operator :code:`//=`.
        """
        res = self.__floordiv__(other)
        self.value = res.value
        return self

    def __mod__(self, other) -> Self:
        """
        Overloading operator :code:`%`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, int):
            res = self.to_native() % other
        elif isinstance(other, BaseDataType):
            res = self.to_native() % other.to_native()
        else:
            self._raise_type_error("%", self, other)

        return self.copy().from_native(res)

    def __imod__(self, other):
        """
        Overloading operator :code:`%=`.
        """
        res = self.__mod__(other)
        self.value = res.value
        return self

    def __pow__(self, other) -> Self:
        """
        Overloading operator :code:`**`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, int):
            res = int(self.to_native() ** other)
        elif isinstance(other, BaseDataType):
            res = int(self.to_native() ** other.to_native())
        else:
            self._raise_type_error("**", self, other)

        return self.copy().from_native(res)

    def __ipow__(self, other):
        """
        Overloading operator :code:`**=`.
        """
        res = self.__pow__(other)
        self.value = res.value
        return self

    def __rshift__(self, other) -> Self:
        """
        Overloading operator :code:`>>`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, int):
            res = self.to_native() >> other
        elif isinstance(other, BaseDataType):
            res = self.to_native() >> other.to_native()
        else:
            self._raise_type_error(">>", self, other)

        return self.copy().from_native(res)

    def __irshift__(self, other):
        """
        Overloading operator :code:`>>=`.
        """
        res = self.__rshift__(other)
        self.value = res.value
        return self

    def __lshift__(self, other) -> Self:
        """
        Overloading operator :code:`<<`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, int):
            res = self.to_native() << other
        elif isinstance(other, BaseDataType):
            res = self.to_native() << other.to_native()
        else:
            self._raise_type_error("<<", self, other)

        return self.copy().from_native(res)

    def __ilshift__(self, other):
        """
        Overloading operator :code:`<<=`.
        """
        res = self.__ilshift__(other)
        self.value = res.value
        return self

    def __and__(self, other) -> Self:
        """
        Overloading operator :code:`&`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, int):
            res = self.value & other
        elif isinstance(other, BaseDataType):
            res = self.value & other.value
        else:
            self._raise_type_error("&", self, other)

        return self.copy().from_native(res)

    def __iand__(self, other):
        """
        Overloading operator :code:`&=`.
        """
        res = self.__and__(other)
        self.value = res.value
        return self

    def __or__(self, other) -> Self:
        """
        Overloading operator :code:`|`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, int):
            res = self.value | other
        elif isinstance(other, BaseDataType):
            res = self.value | other.value
        else:
            self._raise_type_error("|", self, other)

        return self.copy().from_native(res)

    def __ior__(self, other):
        """
        Overloading operator :code:`|=`.
        """
        res = self.__or__(other)
        self.value = res.value
        return self

    def __xor__(self, other) -> Self:
        """
        Overloading operator :code:`^`.
        """
        if self._is_x() or _is_x(other):
            return self.copy().set_x()

        if isinstance(other, int):
            res = self.value ^ other
        elif isinstance(other, BaseDataType):
            res = self.value ^ other.value
        else:
            self._raise_type_error("^", self, other)

        return self.copy().from_native(res)

    def __ixor__(self, other):
        """
        Overloading operator :code:`^=`.
        """
        res = self.__xor__(other)
        self.value = res.value
        return self

    def __lt__(self, other) -> bool:
        """
        Overloading operator :code:`<`.
        """
        if self._is_x() or _is_x(other):
            self._raise_value_error("<")

        if isinstance(other, int):
            res = self.to_native() < other
        elif isinstance(other, BaseDataType):
            res = self.to_native() < other.to_native()
        else:
            self._raise_type_error("<", self, other)

        return res

    def __gt__(self, other) -> bool:
        """
        Overloading operator :code:`>`.
        """
        if self._is_x() or _is_x(other):
            self._raise_value_error(">")

        if isinstance(other, int):
            res = self.to_native() > other
        elif isinstance(other, BaseDataType):
            res = self.to_native() > other.to_native()
        else:
            self._raise_type_error(">", self, other)

        return res

    def __le__(self, other) -> bool:
        """
        Overloading operator :code:`<=`.
        """
        if self._is_x() or _is_x(other):
            self._raise_value_error("<=")

        if isinstance(other, int):
            res = self.to_native() <= other
        elif isinstance(other, BaseDataType):
            res = self.to_native() <= other.to_native()
        else:
            self._raise_type_error("<=", self, other)

        return res

    def __ge__(self, other) -> bool:
        """
        Overloading operator :code:`>=`.
        """
        if self._is_x() or _is_x(other):
            self._raise_value_error(">=")

        if isinstance(other, int):
            res = self.to_native() >= other
        elif isinstance(other, BaseDataType):
            res = self.to_native() >= other.to_native()
        else:
            self._raise_type_error(">=", self, other)

        return res

    def __eq__(self, other) -> bool:
        """
        Overloading operator :code:`==`.
        """
        if self._is_x() or _is_x(other):
            self._raise_value_error("==")

        if isinstance(other, int):
            res = self.to_native() == other
        elif isinstance(other, BaseDataType):
            res = self.to_native() == other.to_native()
        elif isinstance(other, MaskBase):
            res = other == self
        else:
            self._raise_type_error("==", self, other)

        return res

    def __ne__(self, other) -> bool:
        """
        Overloading operator :code:`!=`.
        """
        if self._is_x() or _is_x(other):
            self._raise_value_error("!=")

        if isinstance(other, int):
            res = self.to_native() != other
        elif isinstance(other, BaseDataType):
            res = self.to_native() != other.to_native()
        elif isinstance(other, MaskBase):
            res = other != self
        else:
            self._raise_type_error("!=", self, other)

        return res

    def __neg__(self) -> Self:
        """
        Overloading unary operator :code:`-`.
        """
        if self._is_x():
            return self.copy().set_x()

        res = - self.to_native()
        return self.copy().from_native(res)

    def __pos__(self) -> Self:
        """
        Overloading unary operator :code:`+`.
        """
        return self.copy()

    def __invert__(self) -> Self:
        """
        Overloading unary operator :code:`~`.
        """
        if self._is_x():
            return self.copy().set_x()

        res = ((1 << self.width) - 1) - self.value
        return self.copy().from_native(res)

    def __len__(self) -> int:
        """
        Return length of bit string, used by :code:`len()`.
        """
        return self.width

    def __bool__(self) -> bool:
        """
        Convert value to boolean, used by :code:`bool()`.
        """
        if self._is_x():
            self._raise_value_error("bool")

        return bool(self.to_native())
