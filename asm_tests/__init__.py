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
from .asm_assembly_simple_tests import Asm_Assembly_Simple_Tests
from .asm_assembly_complex_tests import Asm_Assembly_Complex_Tests
