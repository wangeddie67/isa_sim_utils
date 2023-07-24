
# Data Type

Different from math numeric, numbers in ISA always have limited widths and specified formats. In
generic, numbers in computer architecture are defined as below:

- Integer numbers:
  - Signed integer numbers, whose MSB presents the signal of the number while left bits present the
    value of the number.
    - 8-bit/16-bit/32-bit/64-bit signed integer numbers.
  - Unsigned integer numbers, all bit of whom presents the value of the number.
    - 8-bit/16-bit/32-bit/64-bit unsigned integer numbers.
- Fixed-point numbers, whose MSB presents the signal of the number while the higher bits among left 
  bits present the integer part of the value and the lower bits among left bits present the 
  fractional part of the value.
  - The fractional point of the value is maintained by the software. The hardware operation of
    fixed-point numbers is as same as integer numbers. 
- Floating-point numbers, which means the MSB presents the signal of the number, the higher part of
  the left bits define the exponent while the lower part of the left bits present the mantissa.
  - Mantissa means the fraction part of one value among [1,2).
  - Half-precision/Single-precision/Double-precision floating-point number.
  - 8-bit/16-bit floating-point number.

Not all of them are supported efficiently in programming languages, like C/C++ and Python. Hence,
these data types must be redefined in ISA simulators. In general, they should be presented by a bit
string, which presents a number with a limited size. 

Traditionally, the data type for an ISA module has to overload many functions for all kinds of 
operators with different data types. However, aided by the unlimited native data type of Python, 
operators can be performed after converting the bit string to the native data type provided by Python.
After operating, the result can be stored back to the bit string.

Take `SInt8(-5) + SInt8(4)` as example. The values stored in tit strings are `0xFB` and `0x04` 
respectively. Before performing add operation, convert bit strings to native integers as -5 and 1. 
Then, perform add by `-5 + 4` and receive the sum of -1. At last convert the result back to a bit
string, as `0xFF`.

There are some scenarios in which the value of one variable/register does not influence the 
execution of a piece of code, for example, the value of elements of a matrix multiplies. Hence, the 
X state is supported by assigning the bit string as `None`.

## Predefined Data Types

isa_sim_utils provides the following data types:

.. inheritance-diagram:: isa_sim_utils.data_types.base_type isa_sim_utils.data_types.floating isa_sim_utils.data_types.integer

:py:class:`isa_sim_utils.data_types.base_type.BaseDataType` is the abstract base class of data types
that should not be used directly in user codes.

:py:class:`isa_sim_utils.data_types.floating.Floating` provides the base class of floating-point
numbers with configurable width of exponent and mantissa fields.
:py:class:`isa_sim_utils.data_types.integer.SInt` and :py:class:`isa_sim_utils.data_types.integer.UInt`
provides the base class of signed or unsigned integer numbers with configurable bit width. All three
classes can be used within user code with customized widths.

For convenience, functions are provided to generate data type with fixed width:

| Data type | Function | Return value |
| :----: | ---- | ---- |
| 8-bit unsigned integer | :py:func:`isa_sim_utils.data_types.integer.uint8` | :py:class:`isa_sim_utils.data_types.integer.UInt` |
| 16-bit unsigned integer | :py:func:`isa_sim_utils.data_types.integer.uint16` | :py:class:`isa_sim_utils.data_types.integer.UInt` |
| 32-bit unsigned integer | :py:func:`isa_sim_utils.data_types.integer.uint32` | :py:class:`isa_sim_utils.data_types.integer.UInt` |
| 64-bit unsigned integer | :py:func:`isa_sim_utils.data_types.integer.uint64` | :py:class:`isa_sim_utils.data_types.integer.UInt` |
| 8-bit signed integer | :py:func:`isa_sim_utils.data_types.integer.sint8` | :py:class:`isa_sim_utils.data_types.integer.SInt` |
| 16-bit signed integer | :py:func:`isa_sim_utils.data_types.integer.sint16` | :py:class:`isa_sim_utils.data_types.integer.SInt` |
| 32-bit signed integer | :py:func:`isa_sim_utils.data_types.integer.sint32` | :py:class:`isa_sim_utils.data_types.integer.SInt` |
| 64-bit signed integer | :py:func:`isa_sim_utils.data_types.integer.sint64` | :py:class:`isa_sim_utils.data_types.integer.SInt` |
| FP8 (E4M3) | :py:func:`isa_sim_utils.data_types.floating.fp8_e4m3` | :py:class:`isa_sim_utils.data_types.floating.Floating` |
| FP8 (E5M2) | :py:func:`isa_sim_utils.data_types.floating.fp8_e5m2` | :py:class:`isa_sim_utils.data_types.floating.Floating` |
| Float16 | :py:func:`isa_sim_utils.data_types.floating.float16` | :py:class:`isa_sim_utils.data_types.floating.Floating` |
| Half-precision FP | :py:func:`isa_sim_utils.data_types.floating.hpfloat` | :py:class:`isa_sim_utils.data_types.floating.Floating` |
| Single-precision FP | :py:func:`isa_sim_utils.data_types.floating.spfloat` | :py:class:`isa_sim_utils.data_types.floating.Floating` |
| Double-precision FP | :py:func:`isa_sim_utils.data_types.floating.dpfloat` | :py:class:`isa_sim_utils.data_types.floating.Floating` |

## How to Add Variable

It is not suggested to add one data type with only different sizes with `SInt`, `UInt` and 
`Floating`. Instead, it is better to add one function to construct those predefined data types with
fixed arguments if it is essential.

When defining a new data type, except the class declaration and constructor function `__init__`, 
three more functions must be overloaded:

- `copy`: Copy instance of this data.
- `to_native`: Convert the bit string to a value with the native data type of Python, like from
  double-precision number to `float`
- `from_native`: Convert a value with the native data-type of python to the bit string with a
  specified format, like from `float` to double-precision number.

## Unit Test
