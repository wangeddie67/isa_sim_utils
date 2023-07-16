"""
Data structure for AArch64 Register file

This module defines the register file for ARM AArch64 Architecture.

AArch64 Architecture provides:

- 31 64-bit general purpose register.
- 32 scalable vector registers. Width of each register is specified by VL.

  - SIMD&FP registers occupy lower 128 bits of scalable vector registers.

- 16 scalable predicate registers. Width of each register is specified by VL / 8.
- ZA register. (TODO: coming soon)
- ZT0 register. (TODO: coming soon)
- Other registers. (TODO: coming soon)

Each kind of register has dedicated read/write functions.

By default, only predicate registers are initialized. Other registers keep X state. Predicate
registers have three different initialization strategy:

- :code:`ALL_TRUE`: All bits are one, which means all elements are active.
- :code:`ALL_FALSE`: All bits are zero, which means all elements are inactive.
- :code:`RANDOM`: Value of registers is determined by random number, so that some elements are
  active while other elements are inactive.

TODO: register image interface.
"""

from ..data_types import UInt
import random

class ArmRegFile:
    """
    Register file for AArch64.
    """

    r_rf_count = 31
    """
    Count of general purpose registers.
    """
    z_rf_count = 32
    """
    Count of scalable vector registers.
    """
    p_rf_count = 16
    """
    Count of scalable predicate registers.
    """

    def __init__(self,
                 vl: int = 256,
                 predicate_strategy: str = "ALL_TRUE"):
        """
        Construct register file.

        Args:
            vl: vector length in bit of scalable vector register.
            predicate_strategy: strategy to initialize predicate registers. Options:
                :code:`ALL_TRUE`, :code:`ALL_FALSE`, and :code:`RANDOM`. 
        """
        self.vl = vl
        self.r_rf = [UInt(64) for _ in range(0, self.r_rf_count)]
        self.z_rf = [UInt(vl) for _ in range(0, self.z_rf_count)]
        self.p_rf = [UInt(vl // 8) for _ in range(0, self.p_rf_count)]

        if predicate_strategy == "ALL_TRUE":
            self.all_true_predicate()
        elif predicate_strategy == "ALL_FALSE":
            self.all_false_predicate()
        elif predicate_strategy == "RANDOM":
            self.random_predicate()

    def read_r(self, n: int, size: int) -> UInt:
        """
        Read general purpose register. Read register 31 return zero.

        Args:
            n: register index.
            size: read width in bit.

        Return:
            Read data in bit string.
        """
        assert 0 <= n < self.r_rf_count + 1
        if n == 31:
            res = UInt(size, 0)
        else:
            res = self.r_rf[n][size - 1 : 0]
        return res

    def read_v(self, n: int, size: int) -> UInt:
        """
        Read SIMD&FP register.

        Args:
            n: register index.
            size: read width in bit.

        Return:
            Read data in bit string.
        """
        assert 0 <= n < self.z_rf_count
        res = self.z_rf[n][size - 1 : 0]
        return res

    def read_z(self, n: int, size: int) -> UInt:
        """
        Read scalable vector register.

        Args:
            n: register index.
            size: read width in bit.

        Return:
            Read data in bit string.
        """
        assert 0 <= n < self.z_rf_count
        res = self.z_rf[n][size - 1 : 0]
        return res

    def read_p(self, n: int, size: int) -> UInt:
        """
        Read scalable predicate register.

        Args:
            n: register index.
            size: read width in bit.

        Return:
            Read data in bit string.
        """
        assert 0 <= n < self.p_rf_count
        res = self.p_rf[n][size - 1 : 0]
        return res

    def write_r(self, n: int, size: int, value: UInt):
        """
        Write value to general purpose register. Write register 31 performs as NOP.

        Args:
            n: register index.
            size: write width in bit.
            value: write data in bit string.
        """
        assert 0 <= n < self.r_rf_count + 1
        if n == 31:
            pass
        else:
            if isinstance(value, int):
                self.r_rf[n][size - 1 : 0] = value
            else:
                self.r_rf[n][size - 1 : 0] = value.value

    def write_v(self, n: int, size: int, value: UInt):
        """
        Write value to SIMD&FP register.

        Args:
            n: register index.
            size: write width in bit.
            value: write data in bit string.
        """
        assert 0 <= n < self.z_rf_count
        if isinstance(value, int):
            self.z_rf[n][size - 1 : 0] = value
        else:
            self.z_rf[n][size - 1 : 0] = value.value

    def write_z(self, n: int, size: int, value: UInt):
        """
        Write value to scalable vector register.

        Args:
            n: register index.
            size: write width in bit.
            value: write data in bit string.
        """
        assert 0 <= n < self.z_rf_count
        if isinstance(value, int):
            self.z_rf[n][size - 1 : 0] = value
        else:
            self.z_rf[n][size - 1 : 0] = value.value

    def write_p(self, n: int, size: int, value: UInt):
        """
        Write value to scalable predicate register.

        Args:
            n: register index.
            size: write width in bit.
            value: write data in bit string.
        """
        assert 0 <= n < self.p_rf_count
        if isinstance(value, int):
            self.p_rf[n][size - 1 : 0] = value
        else:
            self.p_rf[n][size - 1 : 0] = value.value

    def all_true_predicate(self):
        """
        Set predicate registers to all true.
        """
        predicate_width = self.vl // 8
        all_true_value = (1 << predicate_width) - 1

        for reg in self.p_rf:
            reg[predicate_width - 1: 0] = all_true_value

    def all_false_predicate(self):
        """
        Set predicate registers to all false.
        """
        predicate_width = self.vl // 8
        all_false_value = 0

        for reg in self.p_rf:
            reg[predicate_width - 1: 0] = all_false_value

    def random_predicate(self):
        """
        Set predicate registers to random value.
        """
        predicate_width = self.vl // 8

        for reg in self.p_rf:
            random_value = random.randint(0, 1 << predicate_width)
            reg[predicate_width - 1: 0] = random_value
