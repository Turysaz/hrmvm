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
        mock_store = [-111] # random number
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

    def test_copyfrom_direct_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_COPYFROM, 4, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

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


    def test_copyfrom_indirect_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_COPYFROM_I, 3, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

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

    def test_copyto_direct_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_COPYTO, 4, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

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

    def test_copyto_indirect_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_COPYTO_I, -3, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

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

    def test_bumpup_direct_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_BUMPUP, 4, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

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

    def test_bumpup_indirect_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_BUMPUP_I, 3, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

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

    def test_bumpdwn_direct_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_BUMPDWN, -1, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

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

    def test_bumpdwn_indirect_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_BUMPDWN_I, 3, sut.OPC_NOP]
        sut.ram = [1,2,3,4]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

    def test_add_direct(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_ADD, 0, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.accumulator, 2)

    def test_add_direct_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_ADD, 3, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

    def test_add_indirect(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_ADD_I, 0, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.accumulator, 3)

    def test_add_indirect_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_ADD_I, 2, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

    def test_sub_direct(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_SUB, 0, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.accumulator, 0)

    def test_sub_direct_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_SUB, 3, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

    def test_sub_indirect(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_SUB_I, 0, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.accumulator, -1)

    def test_sub_indirect_invalid_adress(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_SUB_I, 2, sut.OPC_NOP]
        sut.ram = [1,2,3]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidRamAdressException, action)

    def test_jump(self):
        # arrange
        sut = Vm()
        sut.program_count = 1
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMP, 0]

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 0)

    def test_jump_invalid_target(self):
        # arrange
        sut = Vm()
        sut.program_count = 1
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMP, 3]

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidPcException, action)

    def test_jumpz_do_jump(self):
        # arrange
        sut = Vm()
        sut.accumulator = 0
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPZ, 0, sut.OPC_NOP]
        sut.program_count = 1

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 0)

    def test_jumpz_dont_jump(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPZ, 0, sut.OPC_NOP]
        sut.program_count = 1

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 3)

    def test_jumpz_invalid_target_fail(self):
        # arrange
        sut = Vm()
        sut.accumulator = 0
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPZ, 4, sut.OPC_NOP]
        sut.program_count = 1

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidPcException, action)

    def test_jumpz_invalid_target_dont_fail(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPZ, 4, sut.OPC_NOP]
        sut.program_count = 1

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 3)

    def test_jumpn_do_jump(self):
        # arrange
        sut = Vm()
        sut.accumulator = -1
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPN, 0, sut.OPC_NOP]
        sut.program_count = 1

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 0)

    def test_jumpn_dont_jump(self):
        # arrange
        sut = Vm()
        sut.accumulator = 1
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPN, 0, sut.OPC_NOP]
        sut.program_count = 1

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 3)

    def test_jumpn_invalid_target_fail(self):
        # arrange
        sut = Vm()
        sut.accumulator = -4
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPN, 4, sut.OPC_NOP]
        sut.program_count = 1

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidPcException, action)

    def test_jumpn_invalid_target_dont_fail(self):
        # arrange
        sut = Vm()
        sut.accumulator = 4
        sut.rom = [sut.OPC_NOP, sut.OPC_JUMPN, 4, sut.OPC_NOP]
        sut.program_count = 1

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 3)

    def test_jumpa(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_NOP, sut.OPC_NOP, sut.OPC_JUMPA]
        sut.accumulator = 1
        sut.program_count = 2

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.program_count, 1)

    def test_jumpa_invalid_target(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_NOP, sut.OPC_NOP, sut.OPC_JUMPA]
        sut.accumulator = 5
        sut.program_count = 2

        # act
        action = sut.next_step

        # assert
        self.assertRaises(InvalidPcException, action)

    def test_ldpc(self):
        # arrange
        sut = Vm()
        sut.rom = [sut.OPC_NOP, sut.OPC_LDPC, sut.OPC_NOP]
        sut.program_count = 1
        sut.accumulator = -4

        # act
        sut.next_step()

        # assert
        self.assertEqual(sut.accumulator, 1)
        self.assertEqual(sut.program_count, 2)
