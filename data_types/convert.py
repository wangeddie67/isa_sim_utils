"""
Data type conversion

This module defines function to convert between different data types.

For example:

- :code:`convert(int, 1.0)` convert 1.0 to python native integer.
- :code:`convert(float, UInt(8, -1))` convert 0xFF to python native integer.
- :code:`convert(UInt, 1.0, 8)` convert float value 1.0 to unsigned 8-bit integer.
- :code:`convert(dpfloat, UInt(8, -1))` convert integer value 255 to double-precision floating.

"""

from typing import Type, Union, List
from .base_type import BaseDataType

def convert(target: Type,
            value: Union[int, float, BaseDataType],
            *args: List):
    """
    Convert value to specified type.

    Args:
        target: Target data type, int, float or BaseDataType.
        value: Source value.
        args: Arguments for target data type.
    """
    # Native to Native
    if target in [int, float] and isinstance(value, (int, float)):
        if target is int:
            return int(value)
        elif target is float:
            return float(value)

    # Native to BaseDataType
    if isinstance(value, (int, float)):
        return target(*args).from_native(value)

    # BaseDataType to Native
    if target in [int, float] and isinstance(value, BaseDataType):
        if target is int:
            return int(value.to_native())
        elif target is float:
            return float(value.to_native())

    # BaseDataType to Native
    return target(*args).from_native(value.to_native())
