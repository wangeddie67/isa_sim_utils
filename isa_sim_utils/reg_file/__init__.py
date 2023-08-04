"""
Data structure for ISA Register file

This module provides data structures presenting register files of ISA.

Such data structure contains all software-visible registers. Each register is presented as bit
string (:py:class:`UInt`). Each register can be read/write by functions.

By default, each register is X state before any write operation. Register file structure provide 
several strategies to initialize register file, which varies among different ISA. See specified data
structure for initialization strategy.

TODO: register file for other architectures.
TODO: image file interface of register file.
"""

from .arm_regfile import ArmRegFile
