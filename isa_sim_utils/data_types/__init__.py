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

TODO: Fix point data type.
"""

from .base_type import BaseDataType

from .integer import UInt, SInt
from .integer import uint8, uint16, uint32, uint64
from .integer import sint8, sint16, sint32, sint64

from .floating import Floating
from .floating import fp8_e4m3, fp8_e5m2, float16, hpfloat, spfloat, dpfloat

from .convert import convert
