#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# exceptions for the assembler

class AssemblerException(Exception):
    """Base class for all assembler errors"""

    def __init__(self, message=""):
        super().__init__(message)


class AsmSyntaxError(AssemblerException):

    def __init__(self,
            line_nmbr,
            line_content,
            message=""):
        super().__init__(message)

        print("Syntax error in line %i (%s)", (line_nmbr, line_content))
