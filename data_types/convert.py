"""
Data type conversion.
"""

from .base_type import BaseDataType

def convert(target, value, *args):
    """
    Convert value to specified type.

    Args:
        target: Target data type, int, float or other.
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
