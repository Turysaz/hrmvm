#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# asm unit test module

import sys
import os

sys.path.insert(0,
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '../asm')))


from .asm_meta_tests import Asm_Meta_Tests

from .asm_assembly_simple_valid_tests import Asm_Assembly_Simple_Valid_Tests
from .asm_assembly_simple_invalid_tests import Asm_Assembly_Simple_Invalid_Tests

from .asm_assembly_complex_valid_tests import Asm_Assembly_Complex_Valid_Tests
from .asm_assembly_complex_invalid_tests import Asm_Assembly_Complex_Invalid_Tests
