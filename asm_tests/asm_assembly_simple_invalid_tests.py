#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# unit tests for failing (syntax error) single instruction assemblies

import unittest
import hrmasm
from asm_exceptions import *

class Asm_Assembly_Simple_Invalid_Tests(unittest.TestCase):

    def validate_assembly_raises(self, asmcode, expected_exception):
        labels = {}
        action = lambda : hrmasm.assemble(asmcode, labels)
        self.assertRaises(expected_exception, action)


    def test_inbox(self):
        asm = ["INBOX"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_outbox(self):
        asm = ["OUTBOX"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_load(self):
        asm = ["LOAD 3"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_copyfrom_direct(self):
        asm = ["COPYFROM 42"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_copyfrom_indirect(self):
        asm = ["COPYFROM [42]"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_copyto_direct(self):
        asm = ["COPYTO 15"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_copyto_indirect(self):
        asm = ["COPYTO [15]"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_nop(self):
        asm = ["NOP"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_bumpup_direct(self):
        asm = ["BUMPUP 123"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_bumpup_indirect(self):
        asm = ["BUMPUP [123]"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_bumpdwn_direct(self):
        asm = ["BUMPDWN 99"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_bumpdwn_indirect(self):
        asm = ["BUMPDWN [99]"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_add_direct(self):
        asm = ["ADD 5"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_add_indirect(self):
        asm = ["ADD [5]"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_sub_direct(self):
        asm = ["SUB 5"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_sub_indirect(self):
        asm = ["SUB [5]"]
        self.validate_assembly_raises(asm, AsmSyntaxError)

    def test_jump(self):
        asm = ["JUMP testa"]
        lbl = {"testa": 1, "testb": 2}
        self.fail()

    def test_jumpz(self):
        asm = ["JUMPZ testb"]
        lbl = {"testa": 0, "testb": 2}
        self.fail()

    def test_jumpn(self):
        asm = ["JUMPN testb"]
        lbl = {"testa": 1, "testb": 2}
        self.validate_assembly_jmp(asm, lbl, AsmSyntaxError)
        self.fail()

    def test_jumpa(self):
        asm = ["JUMPA"]
        self.validate_assembly_raises(asm, AsmSyntaxError)
        self.fail()

    def test_ldpc(self):
        asm = ["LDPC"]
        self.validate_assembly_raises(asm, AsmSyntaxError)
        self.fail()
