#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# unit tests for single instruction assemblies

import unittest
import hrmasm

class Asm_Assembly_Simple_Valid_Tests(unittest.TestCase):

    def validate_assembly_nojmp(self, asmcode, expected_bytecode):
        labels = {}
        result = hrmasm.assemble(asmcode, labels)
        self.assertEqual(expected_bytecode, result)

    def validate_assembly_jmp(self, asmcode, labels, expected_bytecode):
        result = hrmasm.assemble(asmcode, labels)
        self.assertEqual(expected_bytecode, result)

    def test_inbox(self):
        asm = ["INBOX"]
        exp = [hrmasm.OPC_INBOX]
        self.validate_assembly_nojmp(asm, exp)

    def test_outbox(self):
        asm = ["OUTBOX"]
        exp = [hrmasm.OPC_OUTBOX]
        self.validate_assembly_nojmp(asm, exp)

    def test_load(self):
        asm = ["LOAD 3"]
        exp = [hrmasm.OPC_LOAD, 3]
        self.validate_assembly_nojmp(asm, exp)

    def test_copyfrom_direct(self):
        asm = ["COPYFROM 42"]
        exp = [hrmasm.OPC_COPYFROM, 42]
        self.validate_assembly_nojmp(asm, exp)

    def test_copyfrom_indirect(self):
        asm = ["COPYFROM [42]"]
        exp = [hrmasm.OPC_COPYFROM_I, 42]
        self.validate_assembly_nojmp(asm, exp)

    def test_copyto_direct(self):
        asm = ["COPYTO 15"]
        exp = [hrmasm.OPC_COPYTO, 15]
        self.validate_assembly_nojmp(asm, exp)

    def test_copyto_indirect(self):
        asm = ["COPYTO [15]"]
        exp = [hrmasm.OPC_COPYTO_I, 15]
        self.validate_assembly_nojmp(asm, exp)

    def test_nop(self):
        asm = ["NOP"]
        exp = [hrmasm.OPC_NOP]
        self.validate_assembly_nojmp(asm, exp)

    def test_bumpup_direct(self):
        asm = ["BUMPUP 123"]
        exp = [hrmasm.OPC_BUMPUP, 123]
        self.validate_assembly_nojmp(asm, exp)

    def test_bumpup_indirect(self):
        asm = ["BUMPUP [123]"]
        exp = [hrmasm.OPC_BUMPUP_I, 123]
        self.validate_assembly_nojmp(asm, exp)

    def test_bumpdwn_direct(self):
        asm = ["BUMPDWN 99"]
        exp = [hrmasm.OPC_BUMPDWN, 99]
        self.validate_assembly_nojmp(asm, exp)

    def test_bumpdwn_indirect(self):
        asm = ["BUMPDWN [99]"]
        exp = [hrmasm.OPC_BUMPDWN_I, 99]
        self.validate_assembly_nojmp(asm, exp)

    def test_add_direct(self):
        asm = ["ADD 5"]
        exp = [hrmasm.OPC_ADD, 5]
        self.validate_assembly_nojmp(asm, exp)

    def test_add_indirect(self):
        asm = ["ADD [5]"]
        exp = [hrmasm.OPC_ADD_I, 5]
        self.validate_assembly_nojmp(asm, exp)

    def test_sub_direct(self):
        asm = ["SUB 5"]
        exp = [hrmasm.OPC_SUB, 5]
        self.validate_assembly_nojmp(asm, exp)

    def test_sub_indirect(self):
        asm = ["SUB [5]"]
        exp = [hrmasm.OPC_SUB_I, 5]
        self.validate_assembly_nojmp(asm, exp)

    def test_jump(self):
        asm = ["JUMP testa"]
        lbl = {"testa": 1, "testb": 2}
        exp = [hrmasm.OPC_JUMP, 2]
        self.validate_assembly_jmp(asm, lbl, exp)

    def test_jumpz(self):
        asm = ["JUMPZ testb"]
        lbl = {"testa": 0, "testb": 2}
        exp = [hrmasm.OPC_JUMPZ, 3]
        self.validate_assembly_jmp(asm, lbl, exp)

    def test_jumpn(self):
        asm = ["JUMPN testb"]
        lbl = {"testa": 1, "testb": 2}
        exp = [hrmasm.OPC_JUMPN, 3]
        self.validate_assembly_jmp(asm, lbl, exp)

    def test_jumpa(self):
        asm = ["JUMPA"]
        exp = [hrmasm.OPC_JUMPA]
        self.validate_assembly_nojmp(asm, exp)

    def test_ldpc(self):
        asm = ["LDPC"]
        exp = [hrmasm.OPC_LDPC]
        self.validate_assembly_nojmp(asm, exp)
