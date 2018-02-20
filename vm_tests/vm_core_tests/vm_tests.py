#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# unit test for the vm methods

import sys
sys.path.insert(0, "../vm")

import unittest
from vm_core import Vm

class Vm_Tests(unittest.TestCase):

    def testSomething1(self):
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)

    def testSomething2(self):
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)

    def testSomething3(self):
        self.assertTrue(1 == 1)
        self.assertFalse(1 == 2)
