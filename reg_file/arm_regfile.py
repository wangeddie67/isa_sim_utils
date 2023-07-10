"""
ARM register file definition
"""

from ..data_types import UInt
import random

class ArmRegFile:
    """
    Base register file.

    Define access functions.
    """
    r_rf_count = 31
    z_rf_count = 32
    p_rf_count = 16

    def __init__(self,
                 vl: int = 256,
                 predicate_strategy: str = "ALL_TRUE",
                 data_file_path: str = None):
        self.vl = vl
        self.r_rf = [UInt(64, 0) for _ in range(0, self.r_rf_count)]
        self.z_rf = [UInt(vl, 0) for _ in range(0, self.z_rf_count)]
        self.p_rf = [UInt(vl // 8, 0) for _ in range(0, self.p_rf_count)]

        if predicate_strategy == "ALL_TRUE":
            self.all_true_predicate()
        elif predicate_strategy == "ALL_FALSE":
            self.all_false_predicate()
        elif predicate_strategy == "RANDOM":
            self.random_predicate()

    def read_r(self, n: int, size: int):
        assert 0 <= n < self.r_rf_count + 1
        if n == 31:
            res = UInt(size, 0)
        else:
            res = UInt(size, self.r_rf[n][size - 1 : 0])
        return res

    def read_v(self, n: int, size: int):
        assert 0 <= n < self.z_rf_count
        res = UInt(size, self.z_rf[n][size - 1 : 0])
        return res

    def read_z(self, n: int, size: int):
        assert 0 <= n < self.z_rf_count
        res = UInt(size, self.z_rf[n][size - 1 : 0])
        return res

    def read_p(self, n: int, size: int):
        assert 0 <= n < self.p_rf_count
        res = UInt(size, self.p_rf[n][size - 1 : 0])
        return res

    def write_r(self, n: int, size: int, value: UInt):
        assert 0 <= n < self.r_rf_count + 1
        if n == 31:
            pass
        else:
            if isinstance(value, int):
                self.r_rf[n][size - 1 : 0] = value
            else:
                self.r_rf[n][size - 1 : 0] = value.value

    def write_v(self, n: int, size: int, value: UInt):
        assert 0 <= n < self.z_rf_count
        if isinstance(value, int):
            self.z_rf[n][size - 1 : 0] = value
        else:
            self.z_rf[n][size - 1 : 0] = value.value

    def write_z(self, n: int, size: int, value: UInt):
        assert 0 <= n < self.z_rf_count
        if isinstance(value, int):
            self.z_rf[n][size - 1 : 0] = value
        else:
            self.z_rf[n][size - 1 : 0] = value.value

    def write_p(self, n: int, size: int, value: UInt):
        assert 0 <= n < self.p_rf_count
        if isinstance(value, int):
            self.p_rf[n][size - 1 : 0] = value
        else:
            self.p_rf[n][size - 1 : 0] = value.value

    def all_true_predicate(self):
        predicate_width = self.vl // 8
        all_true_value = (1 << predicate_width) - 1

        for reg in self.p_rf:
            reg[predicate_width - 1: 0] = all_true_value

    def all_false_predicate(self):
        predicate_width = self.vl // 8
        all_false_value = 0

        for reg in self.p_rf:
            reg[predicate_width - 1: 0] = all_false_value

    def random_predicate(self):
        predicate_width = self.vl // 8

        for reg in self.p_rf:
            random_value = random.randint(0, 1 << predicate_width)
            reg[predicate_width - 1: 0] = random_value
