"""
It is very basic work in ISA modules to define data structure for different data format, like 
Int8, Int16, FP8, DP and so on. This package provides data structures to present a data with 
limitation of bit width and formats.

The kernel data structure is a bit string presented in one integer, as
:py:attr:`BaseDataType._value`. This takes the advantage of unlimited width of native data type
provided by python.

Traditionally, data type for ISA module have to overload many functions for all kinds of operators
with different kind of data type. However, aided by the unlimited native data type of python, 
operators can be performed after convert bit string to native data type of python. Then, the result
can be stored back to bit string.

Take :code:`SInt8(-5) + SInt8(4)` as example. The values stored in bit string are :code:`0xFB` and
:code:`0x04` respectively. Before perform operation, convert bit string to native integer as -5 and
4. Then, perform add by :code:`-5 + 4` and receive sum of -1. At last convert the result back to bit
string, as :code:`0xFF`.

There are some situation that the value does not influence the execution of a piece of code. Hence,
X state is support by assigning the bit string as :code:`None`.
"""

from .base_type import BaseDataType

from .integer import Integer
from .integer import UInt, UInt8, UInt16, UInt32, UInt64
from .integer import SInt, SInt8, SInt16, SInt32, SInt64

from .floating import Floating
from .floating import FP8E4M3, FP8E5M2, Float16, HpFloat, SpFloat, DpFloat

from .convert import convert
