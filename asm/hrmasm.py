#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
# Assembler for .hasm assembercode files


# TODO: improve the label thing. what an inperformant hack!

import sys
import re

helpstr="""Usage:
hrmasm [<options>] <assemblyfile>

options:
-o <file>       output file
-a              ascii output
-h              show this text
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


def clean(lines):
    re_cmnt = re.compile(r";.*")
    re_empty = re.compile(r"\s+")
    ret = []
    for line in lines:
        line = re_cmnt.sub("", line)
        line = re_empty.sub(" ", line)
        line = line.strip()
        if line == "":
            continue
        ret.append(line)
    return ret

def find_and_remove_labels(lines):
    ret_lines = []
    labeltable = {}
    i = 0
    for line in lines:
        if line[-1] == ":":
            if " " in line:
                print("SYNTAX ERROR IN LINE:")
                print(line)
                sys.exit()
            #label found
            labeltable.update({line[:-1]: i})
        else:
            i += 1
            ret_lines.append(line)
    # end for
    return (ret_lines, labeltable)


    return (lines,dict()) #(str:int), lab: pc

def syntax_error(msg, line):
    print("Syntax error")
    print(msg + "(line " + str(line) +")")
    sys.exit()

def assemble(lines, labels):
    bytecode = []

    # hack
    calltable = {}
    for lbl in labels:
        calltable.update({lbl: []})

    line_number = -1 # for debug messages
    line_index = 0
    for line in lines:

        line_number += 1

        frags = line.split()
        indirect = True if len(frags) > 1 and frags[1][0] == "[" else False

        # hack
        if len(frags) > 1:
            #print("at line " + line)
            for lb in labels:
                if labels[lb] > line_index:
                    #print("shifting " + lb + " by " + str(len(frags) -1))
                    labels[lb] += len(frags) - 1
        line_index += len(frags)

        word = frags[0].lower()

        if word == "inbox":
            if len(frags) != 1:
                syntax_error("INBOX does not have arguments.", line_number)

            bytecode.append(OPC_INBOX)
            continue

        if word == "outbox":
            if len(frags) != 1:
                syntax_error("OUTBOX does not have arguments.", line_number)

            bytecode.append(OPC_OUTBOX)
            continue

        if word == "load":
            if len(frags) != 2:
                syntax_error("LOAD takes 1 argument", line_number)

            bytecode.append(OPC_LOAD)

        if word == "copyfrom":
            if len(frags) != 2:
                syntax_error("COPYFROM takes 1 argument", line_number)

            if indirect:
                bytecode.append(OPC_COPYFROM_I)
            else:
                bytecode.append(OPC_COPYFROM)

        if word == "copyto":
            if len(frags) != 2:
                syntax_error("COPYTO takes 1 argument", line_number)

            if indirect:
                bytecode.append(OPC_COPYTO_I)
            else:
                bytecode.append(OPC_COPYTO)

        if word == "nop":
            bytecode.append(OPC_NOP)
            continue

        if word == "bumpup":
            if len(frags) != 2:
                syntax_error("BUMPUP takes 1 argument", line_number)

            if indirect:
                bytecode.append(OPC_BUMPUP_I)
            else:
                bytecode.append(OPC_BUMPUP)

        if word == "bumpdwn":
            if len(frags) != 2:
                syntax_error("BUMPDWN takes 1 argument", line_number)

            if indirect:
                bytecode.append(OPC_BUMPDWN_I)
            else:
                bytecode.append(OPC_BUMPDWN)

        if word == "add":
            if len(frags) != 2:
                syntax_error("ADD takes 1 argument", line_number)

            if indirect:
                bytecode.append(OPC_ADD_I)
            else:
                bytecode.append(OPC_ADD)

        if word == "sub":
            if len(frags) != 2:
                syntax_error("SUB takes 1 argument", line_number)

            if indirect:
                bytecode.append(OPC_SUB_I)
            else:
                bytecode.append(OPC_SUB)

        if word == "jump":
            if len(frags) != 2:
                syntax_error("JUMP takes 1 argument", line_number)

            bytecode.append(OPC_JUMP)
            calltable[frags[1]].append(len(bytecode))
            bytecode.append(-1)
            continue

        if word == "jumpz":
            if len(frags) != 2:
                syntax_error("JUMPZ takes 1 argument", line_number)

            bytecode.append(OPC_JUMPZ)
            calltable[frags[1]].append(len(bytecode))
            bytecode.append(-1)
            continue

        if word == "jumpn":
            if len(frags) != 2:
                syntax_error("JUMPN takes 1 argument", line_number)

            bytecode.append(OPC_JUMPN)
            calltable[frags[1]].append(len(bytecode))
            bytecode.append(-1)
            continue

        if word == "jumpa":
            if len(frags) != 1:
                syntax_error("JUMPA takes no arguments!", line_number)

            bytecode.append(OPC_JUMPA)
            continue

        if word == "ldpc":
            if len(frags) != 1:
                sytax_error("LDPC takes no arguments!", line_number)
            bytecode.append(OPC_LDPC)
            continue


        # add argument to bytecode
        if len(frags) > 1:
            if indirect:
                bytecode.append(int(frags[1][1:-1])) # remove brackets
            else:
                bytecode.append(int(frags[1]))

    for lbl in calltable:
        for call in calltable[lbl]:
            bytecode[call] = labels[lbl]

    return bytecode

def write_bytes(bytecode, path, oascii):
    if oascii:
        ofile = open(path, "w")
        lindex = 0
        for b in bytecode:
            ofile.write(("%0.2X" % b))
            lindex += 1
            if lindex == 16:
                lindex = 0
                ofile.write("\n")
            else:
                ofile.write(" ")
        ofile.close()
    else:
        ofile = open(path, "wb")
        ofile.write(bytes(bytecode))
        ofile.close()

def settings(args):
    ifile = None
    ofile = "out.hrmbin"
    oascii = False

    while len(args) > 0:
        if args[0] == "-o":
            if len(args) < 2:
                print("syntax error")
                sys.exit()
            ofile = args[1]
            args = args[2:]
            continue

        if args[0] == "-a":
            oascii = True
            args = args[1:]

        if args[0] == "-h":
            print(helpstr)
            sys.exit()

        if args[0][0] == "-":
            print("unknown option: " + args[0])
            sys.exit()

        ifile = args[0]
        args = args[1:]

    if ifile == None:
        print("Specify input file!")
        print(helpstr)
        sys.exit()

    return (ifile, ofile, oascii)

def mainloop(args):
    ifile, ofile, oascii = settings(args)
    ifile = open(ifile)
    lines = [l.strip() for l in ifile.readlines()]

    lines = clean(lines)
    (lines, lbls) = find_and_remove_labels(lines)
    bytecode = assemble(lines, lbls)

    write_bytes(bytecode, ofile, oascii)


mainloop(sys.argv[1:])
