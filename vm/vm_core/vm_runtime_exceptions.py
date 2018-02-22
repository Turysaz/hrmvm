#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# VM Runtime Exception classes

class VmRuntimeError(Exception):
    "Base class for all CPU-crashing cases like PC < 0 or similar."

    def __init__(self, message=""):
        super().__init__(message)


class InvalidPcException(VmRuntimeError):
    "Error to throw if the PC value (actual or to-be-set) is invalid (e.g. < 0)"

    def __init__(self, pc, message=""):
        super().__init__(message)
        print("PC = " + str(pc))

class InvalidRamAdressException(VmRuntimeError):
    "Error to throw if the RAM adress is invalid"

    def __init__(self, adress, message=""):
        super().__init__(message)
        print("Adress = " + str(adress))

class NoRomException(VmRuntimeError):
    "Error to throw if the ROM is None or has length 0"

    def __init__(self, message=""):
        super().__init__(message)

class UnknownOpCodeException(VmRuntimeError):
    "Exception to throw if an unknown opcode is called."

    def __init__(self, opcode, message=""):
        super().__init__(message)
        print("Opcode = " + str(opcode))
