"""
Mask bit vector.

TODO: check with softfloat.
"""

from typing_extensions import Self

class MaskBase:
    """
    Mask integer.

    Width is configurable.
    """
    def __init__(self, width: int, value: int, mask: int):
        """
        Construct one data.

        Args:
            width: Width in bit.
            value: Bit string.
            mask: Mask bit string.
        """
        self.width = width
        self.value = value
        self.mask = mask

    def copy(self) -> Self:
        """
        Copy instance of this data.

        Args:
            width: overwrite width of bit string.
        """
        return MaskBase(self.width, self.value, self.mask)


    def __eq__(self, other) -> bool:
        """
        Overloading operator :code:`==`.
        """
        return (other & self.mask) == self.value

    def __ne__(self, other) -> bool:
        """
        Overloading operator :code:`!=`.
        """
        return (other & self.mask) != self.value

