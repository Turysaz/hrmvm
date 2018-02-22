#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# HRMVM machine simulation

import queue
import sys

from .vm_runtime_exceptions import *

class Vm():
    """
    The heart of the emulation.
    Contains Registers, RAM, ROM.
    """

    # opcodes
    OPC_INBOX       = 0x00
    OPC_OUTBOX      = 0x01
    OPC_LOAD        = 0x02
    OPC_COPYFROM    = 0x03
    OPC_COPYFROM_I  = 0x04
    OPC_COPYTO      = 0x05
    OPC_COPYTO_I    = 0x06
    OPC_NOP         = 0x07
    OPC_BUMPUP      = 0x08
    OPC_BUMPUP_I    = 0x09
    OPC_BUMPDWN     = 0x0a
    OPC_BUMPDWN_I   = 0x0b
    OPC_ADD         = 0x0c
    OPC_ADD_I       = 0x0d
    OPC_SUB         = 0x0e
    OPC_SUB_I       = 0x0f
    OPC_JUMP        = 0x10
    OPC_JUMPZ       = 0x11
    OPC_JUMPN       = 0x12
    OPC_JUMPA       = 0x13
    OPC_LDPC        = 0x14


    def __init__(self, ram_size=255):

        self.program_count = 0
        self.accumulator = 0
        self.ram = [0 for x in range(ram_size)]
        self.rom = None

        self.istream = queue.Queue()
        self.ostream = queue.Queue()

        # attach functions here to receive i/ostream writes
        # e.g.: vm.ostream_subscribers.append(self.write_vm_ostream)
        # (subscribers need to have one parameter for the written value)
        self.istream_subscribers = []
        self.ostream_subscribers = []

        self.opcode_handlers = {
            self.OPC_INBOX:     self.op_pop_inbox,
            self.OPC_OUTBOX:    self.op_push_outbox,
            self.OPC_LOAD:      self.op_load,
            self.OPC_COPYFROM:  self.op_copyfrom_direct,
            self.OPC_COPYFROM_I:self.op_copyfrom_indirect,
            self.OPC_COPYTO:    self.op_copyto_direct,
            self.OPC_COPYTO_I:  self.op_copyto_indirect,
            self.OPC_NOP:       self.op_nop,
            self.OPC_BUMPUP:    self.op_bumpup_direct,
            self.OPC_BUMPUP_I:  self.op_bumpup_indirect,
            self.OPC_BUMPDWN:   self.op_bumpdwn_direct,
            self.OPC_BUMPDWN_I: self.op_bumpdwn_indirect,
            self.OPC_ADD:       self.op_add_direct,
            self.OPC_ADD_I:     self.op_add_indirect,
            self.OPC_SUB:       self.op_sub_direct,
            self.OPC_SUB_I:     self.op_sub_indirect,
            self.OPC_JUMP:      self.op_jump,
            self.OPC_JUMPZ:     self.op_jumpz,
            self.OPC_JUMPN:     self.op_jumpn,
            self.OPC_JUMPA:     self.op_jumpa,
            self.OPC_LDPC:      self.op_load_pc
        }

    # end ctor

    def next_step(self):

        if self.rom == None or len(self.rom) == 0:
            raise NoRomException()

        if self.program_count < 0 or self.program_count > len(self.rom):
            raise InvalidPcException(self.program_count)

        instr = self.rom[self.program_count]
        self.program_count += 1

        if instr not in self.opcode_handlers:
            raise UnknownOpCodeException(instr)

        self.opcode_handlers[instr]()

        if self.program_count == len(self.rom):
            print("Warning: PC out of range! Setting PC to zero.\n" +
                  "If you want to create a loop, you should consider\n" +
                  "doing so explicitely!")
            self.program_count = 0

    # end next_step()

    # ---- AUX ----

    def load_direct(self, adress):
        self.evaluate_valid_ram_cell(adress)
        return self.ram[adress]

    def load_indirect(self, adress):
        self.evaluate_valid_ram_cell(adress)
        self.evaluate_valid_ram_cell(self.ram[adress])
        return self.ram[self.ram[adress]]

    def store_direct(self, adress, value):
        self.evaluate_valid_ram_cell(adress)
        self.ram[adress] = value

    def store_indirect(self, adress, value):
        self.evaluate_valid_ram_cell(adress)
        self.ram[self.ram[adress]] = value

    def evaluate_valid_pc(self, pc):
        if pc >= len(self.rom) or pc < 0:
            raise InvalidPcException(pc)

    def evaluate_valid_ram_cell(self, adress):
        if adress >= len(self.ram) or adress < 0:
            raise InvalidRamAdressException(adress)

    # ---- OPC ----

    def op_pop_inbox(self):
        if self.istream.empty():
            print("No values in istream! Assuming zero.")
            self.accumulator = 0
        else:
            self.accumulator = self.istream.get()

        for subscr in self.istream_subscribers:
            subscr(self.accumulator)

    def op_push_outbox(self):
        self.ostream.put(self.accumulator)
        for subscr in self.ostream_subscribers:
            subscr(self.accumulator)
        self.accumulator = 0

    def op_load(self):
        self.accumulator = self.rom[self.program_count]
        self.program_count += 1

    def op_copyfrom_direct(self):
        p = self.rom[self.program_count]
        self.accumulator = self.load_direct(p)
        self.program_count += 1

    def op_copyfrom_indirect(self):
        p = self.rom[self.program_count]
        self.accumulator = self.load_indirect(p)
        self.program_count += 1

    def op_copyto_direct(self):
        p = self.rom[self.program_count]
        self.store_direct(p, self.accumulator)
        self.program_count += 1

    def op_copyto_indirect(self):
        p = self.rom[self.program_count]
        self.store_indirect(p, self.accumulator)
        self.program_count += 1

    def op_nop(self):
        pass

    def op_bumpup_direct(self):
        p = self.rom[self.program_count]
        self.accumulator = self.load_direct(p) + 1
        self.store_direct(p, self.accumulator)
        self.program_count += 1

    def op_bumpup_indirect(self):
        p = self.rom[self.program_count]
        self.accumulator = self.load_indirect(p) + 1
        self.store_indirect(p, self.accumulator)
        self.program_count += 1

    def op_bumpdwn_direct(self):
        p = self.rom[self.program_count]
        self.accumulator = self.load_direct(p) - 1
        self.store_direct(p, self.accumulator)
        self.program_count += 1

    def op_bumpdwn_indirect(self):
        p = self.rom[self.program_count]
        self.accumulator = self.load_indirect(p) - 1
        self.store_indirect(p, self.accumulator)
        self.program_count += 1

    def op_add_direct(self):
        p = self.rom[self.program_count]
        self.accumulator += self.load_direct(p)
        self.program_count += 1

    def op_add_indirect(self):
        p = self.rom[self.program_count]
        self.accumulator += self.load_indirect(p)
        self.program_count += 1

    def op_sub_direct(self):
        p = self.rom[self.program_count]
        self.accumulator -= self.load_direct(p)
        self.program_count += 1

    def op_sub_indirect(self):
        p = self.rom[self.program_count]
        self.accumulator -= self.load_indirect(p)
        self.program_count += 1

    def op_jump(self):
        p = self.rom[self.program_count]
        self.evaluate_valid_pc(p)
        self.program_count = p

    def op_jumpz(self):
        p = self.rom[self.program_count]
        if self.accumulator == 0:
            self.evaluate_valid_pc(p)
            self.program_count = p
        else:
            self.program_count += 1

    def op_jumpn(self):
        p = self.rom[self.program_count]
        if self.accumulator < 0:
            self.evaluate_valid_pc(p)
            self.program_count = p
        else:
            self.program_count += 1

    def op_jumpa(self):
        self.evaluate_valid_pc(self.accumulator)
        self.program_count = self.accumulator

    def op_load_pc(self):
        self.accumulator = self.program_count - 1
