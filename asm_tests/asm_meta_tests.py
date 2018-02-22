#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# unit tests for the assembler meta functionality


import unittest
import hrmasm

class Asm_Meta_Tests(unittest.TestCase):

    def test_cleaning(self):
        # arrange
        original = [
            "; some commentary",
            "LOAD    1 ; a line",
            "ADD 0;  ",
            "   SUB 1   ",
            "; c ; o ; m ; m ; e ; n ; t ; s",
            "   ",
            "",
            "lbl:   ",
            " another_lbl:",
            "JUMP  \t  0"
        ]

        expected = [
            "LOAD 1",
            "ADD 0",
            "SUB 1",
            "lbl:",
            "another_lbl:",
            "JUMP 0"
        ]

        # act
        result = hrmasm.clean(original)

        # assert
        self.assertEqual(result, expected)

    def test_find_remove_labels(self):
        # arrange
        original =[
            "LBL1:",
            "LOAD 1",
            "LBL2:",
            "ADD 0",
            "SUB 1",
            "JUMPZ LBL2",
            "LBL3:",
            "JUMP LBL1"
        ]
        expected = [
            "LOAD 1",
            "ADD 0",
            "SUB 1",
            "JUMPZ LBL2",
            "JUMP LBL1"
        ]
        exp_table = {
            "LBL1" : 0,
            "LBL2" : 1,
            "LBL3" : 4
        }

        # act
        res_lines, res_tab = hrmasm.find_and_remove_labels(original)

        # assert
        self.assertEqual(res_lines, expected)
        self.assertEqual(res_tab, exp_table)

    def test_settings_default(self):
        # arrange
        args = ["a"]

        # act
        ifile, ofile, oascii = hrmasm.settings(args)

        # assert
        self.assertEqual(ifile, "a")
        self.assertEqual(ofile, "out.hrmasm")
        self.assertEqual(oascii, False)

    def test_settings_default(self):
        # arrange
        args = ["-o", "o", "a"]

        # act
        ifile, ofile, oascii = hrmasm.settings(args)

        # assert
        self.assertEqual(ifile, "a")
        self.assertEqual(ofile, "o")
        self.assertEqual(oascii, False)

    def test_settings_default(self):
        # arrange
        args = ["-o", "o", "-a", "a"]

        # act
        ifile, ofile, oascii = hrmasm.settings(args)

        # assert
        self.assertEqual(ifile, "a")
        self.assertEqual(ofile, "o")
        self.assertEqual(oascii, True)
