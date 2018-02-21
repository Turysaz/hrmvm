#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# unit test for the vm methods


import unittest
from vm_core import Vm
from vm_core.vm_runtime_exceptions import *


class Vm_Opcode_Tests(unittest.TestCase):

    # === OPCODE HANDLERS ===

    def test_pop_inbox(self):
        # arrange
        mock_store = [-111] # reference type
        def mock(x):
            mock_store[0] = x

        sut = Vm()
        sut.rom = [sut.OPC_INBOX, sut.OPC_NOP]
        sut.istream.put(42)

        sut.istream_subscribers.append(mock)

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 1)
        self.assertEqual(sut.accumulator, 42)
        self.assertEqual(mock_store[0], 42) # mock called

    def test_push_outbox(self):
        # arrange
        mock_store = [-143] # random number
        def mock(x):
            mock_store[0] = x

        sut = Vm()
        sut.rom = [sut.OPC_OUTBOX, sut.OPC_NOP]
        sut.ostream_subscribers.append(mock)
        sut.accumulator = 42

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 1)
        self.assertEqual(sut.accumulator, 0)
        self.assertEqual(mock_store[0], 42) # mock called


    def test_load(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_LOAD, 42, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 42)

    def test_copyfrom_direct(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_COPYFROM, 2, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 3)
        self.assertEqual(sut.ram, [1,2,3,4])

    def test_copyfrom_indirect(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_COPYFROM_I, 2, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 4)
        self.assertEqual(sut.ram, [1,2,3,4])

    def test_copyto_direct(self):
        # arrange
        sut = Vm()
        sut.accumulator = 42
        sut.rom = [sut.OPC_COPYTO, 2, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 42)
        self.assertEqual(sut.ram[2], 42)

    def test_copyto_indirect(self):
        # arrange
        sut = Vm()
        sut.accumulator = 42
        sut.ram = [1,2,3,4]
        sut.rom = [sut.OPC_COPYTO_I, 2, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 42)
        self.assertEqual(sut.ram, [1,2,3,42])

    def test_nop(self):
        # arrange
        sut = Vm()
        sut.accumulator = 42
        sut.ram = [1,2,3,4]
        sut.rom = [sut.OPC_NOP, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 1)
        self.assertEqual(sut.accumulator, 42)
        self.assertEqual(sut.ram, [1,2,3,4])

    def test_bumpup_direct(self):
        # arrange
        sut = Vm()
        sut.accumulator = 42
        sut.ram = [1,2,3,4]
        sut.rom = [sut.OPC_BUMPUP, 2, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 4)
        self.assertEqual(sut.ram, [1,2,4,4])

    def test_bumpup_indirect(self):
        # arrange
        sut = Vm()
        sut.accumulator = 42
        sut.ram = [1,2,3,4]
        sut.rom = [sut.OPC_BUMPUP_I, 2, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 5)
        self.assertEqual(sut.ram, [1,2,3,5])

    def test_bumpdwn_direct(self):
        # arrange
        sut = Vm()
        sut.accumulator = 42
        sut.ram = [1,2,3,4]
        sut.rom = [sut.OPC_BUMPDWN, 2, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 2)
        self.assertEqual(sut.ram, [1,2,2,4])

    def test_bumpdwn_indirect(self):
        # arrange
        sut = Vm()
        sut.accumulator = 42
        sut.ram = [1,2,3,4]
        sut.rom = [sut.OPC_BUMPDWN_I, 2, sut.OPC_NOP]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 2)
        self.assertEqual(sut.accumulator, 3)
        self.assertEqual(sut.ram, [1,2,3,3])

    def test_add_direct(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_test_indirect(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_sub_direct(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_sub_indirect(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_jump(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_jumpz(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_jumpn(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_jumpa(self):
        # arrange
        # act
        # assert
        self.fail()

    def test_ldpc(self):
        # arrange
        # act
        # assert
        self.fail()
