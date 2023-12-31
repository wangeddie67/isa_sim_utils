"""
Test data types.
"""

import os
import sys
path = sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

import unittest  # pylint: disable=wrong-import-position
from isa_sim_utils.data_types import UInt, float16, convert # pylint: disable=wrong-import-position

class TestInteger(unittest.TestCase):
    """
    Test data type.
    """

    def test_add(self):
        a = UInt(8, 8)
        b = UInt(8, 10)
        self.assertEqual((a + b).to_native(), 18)
        self.assertEqual((a - b).to_native(), 256 - 2)
        self.assertEqual((a * b).to_native(), 80)
        self.assertEqual((a / b).to_native(), 0)
        self.assertEqual((a % b).to_native(), 8)
        self.assertEqual(hex(a), '0x8')

    def test_convert(self):
        a = UInt(8, 8)
        b = float16(1.5)
        self.assertEqual(convert(float, a), 8.0)
        self.assertEqual(convert(int, b), 1)

if __name__ == '__main__':
    unittest.main()
