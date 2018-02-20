#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# unit tests for the assembler

import sys
sys.path.insert(0, "../asm")

import unittest
import hrmasm

class Hrmasm_Tests(unittest.TestCase):

    def test_me(self):
        self.assertEqual(1,1)
