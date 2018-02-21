#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# unit test for the vm methods


import unittest
from vm_core import Vm
from vm_core.vm_runtime_exceptions import *

class Vm_Basic_Tests(unittest.TestCase):

    # === INITIALIZATION ===

    def test_initialization_default_values(self):
        # arrange / act
        sut = Vm()

        # assert
        self.assertEqual(sut.accumulator, 0)
        self.assertEqual(sut.program_count, 0)
        self.assertEqual(len(sut.ram), 255)
        self.assertIsNone(sut.rom)

    def test_initialization_custom_ram_size(self):
        # arrange / act
        sut = Vm(10)

        # assert
        self.assertEqual(len(sut.ram), 10)

    # === NEXT STEP ===

    def test_next_step_no_rom_raise_NoRomException(self):
        # arrange
        sut = Vm()

        # act
        action = sut.next_step

        # assert
        self.assertRaises(NoRomException, action)

    def test_next_step_invalid_opcode_UnknownOpcodeException(self):
        # arrange
        sut = Vm()
        sut.rom = [255]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(UnknownOpCodeException, action)

    def test_next_step_pc_negative_InvalidPcException(self):
        # arrange
        sut = Vm()
        sut.rom = [7,7,7]
        sut.program_count = -1

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidPcException, action)

    def test_next_step_pc_larger_than_rom_InvalidPcException(self):
        # arrange
        sut = Vm()
        sut.rom = [7,7,7]
        sut.program_count = 4

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidPcException, action)

    def text_next_step_everything_okay(self):
        # arrange
        sut = Vm()
        sut.rom = [7,7,7]

        # action
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 1)
