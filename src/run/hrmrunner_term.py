#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# terminal based runner for hrm programs

import sys
import time

sys.path.insert(0, "src/vm")
from hrmvm import HrmVm as VM

def print_vm(vm):
    print("PC:  " + str(vm.program_count) + ",  " +
          "ACC: " + str(vm.accumulator))
    print("RAM: " + str(vm.ram))
    print("\n")

def readbin(filepath):
    infile = open(filepath, "rb")
    data = infile.read()
    infile.close()
    ret = []
    for b in data:
        ret.append(int(b))
    return ret

def ostream_emulation(val):
    print("VAL WRITTEN: " + str(val))

vm = VM(ram_size=10)

vm.rom = [8,0,8,1,10,2,16,0]

#vm.rom = [2,11,5,0, 2,13,5,1, 2,-20,5,2, # load initial
#          2,2,5,4, # load 2 to [4]
#          9,4,     # incr [[4]]
#          10,4,    # decr [4]
#          18,12,   # jumpn 12
#          16,16]   # jump 16

data = readbin(sys.argv[1])
vm.rom = data

vm.ostream_subscribers.append(ostream_emulation)

while(True):
    print_vm(vm)
    #input("enter for next step")
    time.sleep(0.1)
    vm.next_step()
