#!/usr/bin/python3

# Copyright (c) Turysaz 2018
# This file is part of the HRMVM toolkit
# HRMVM is free software. See LICENSE file for further information
#
#
# Minimalistic GUI representation for HRMVM

import sys

from vm_core import Vm

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox, QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

def bytestr(i):
    return str(i)
    #return ("0x%0.2X" % i)

def readbin(filepath):
    infile = open(filepath, "rb")
    data = infile.read()
    infile.close()
    ret = []
    for b in data:
        ret.append(int(b))
    return ret

class App(QMainWindow):

    def __init__(self, vm_ram_size, rom):
        super().__init__()

        self.title = 'HRM VM'
        self.left = 10
        self.top = 10
        self.width = 350
        self.height = 500

        self.vm = Vm(ram_size=vm_ram_size)
        self.vm.rom = rom
        self.vm.ostream_subscribers.append(self.ostream_append)

        self.initUI()

    def ostream_append(self, out):
        self.ostream_val.setText(self.ostream_val.text() + " " + str(out))


    def initUI(self):

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        # immutable components
        acc_lbl = QLabel(self)
        acc_lbl.move(130, 100)
        acc_lbl.setText("ACC:")
        pc_lbl = QLabel(self)
        pc_lbl.move(130, 70)
        pc_lbl.setText("PC:")

        ostream_lbl = QLabel(self)
        ostream_lbl.move(20,40)
        ostream_lbl.setText("Out:")

        istream_lbl = QLabel(self)
        istream_lbl.move(20,15)
        istream_lbl.setText("In:")

        ram_lbl = QLabel(self)
        ram_lbl.move(240, 70)
        ram_lbl.setText("RAM:")

        ram_lbls = [QLabel(self) for i in range(len(self.vm.ram))]
        for i in range(len(self.vm.ram)):
            ram_lbls[i].move(240, 95 + 15 * i)
            ram_lbls[i].setText(bytestr(i) + ":")

        rom_vals = [QLabel(self) for i in range(len(self.vm.rom))]
        for i in range(len(self.vm.rom)):
            rom_vals[i].move(80, 95 + 15 * i)
            rom_vals[i].setText(bytestr(self.vm.rom[i]))


        # mutable components
        self.ostream_val = QLabel(self)
        self.ostream_val.move(50, 40)

        self.istream_val = QLabel(self)
        self.istream_val.move(50, 15)
        self.istream_val.setText("dummy")

        self.acc_val = QLabel(self)
        self.acc_val.move(170, 100)

        self.pc_val = QLabel(self)
        self.pc_val.move(170, 70)

        self.ram_vals = [QLabel(self) for i in range(len(self.vm.ram))]
        for i in range(len(self.vm.ram)):
            self.ram_vals[i].move(300, 95 + 15 * i)

        rom_lbl = QLabel(self)
        rom_lbl.move(30, 70)
        rom_lbl.setText("ROM:")

        self.rom_lbls = [QLabel(self) for i in range(len(self.vm.rom))]
        for i in range(len(self.vm.rom)):
            self.rom_lbls[i].move(30, 95 + 15 * i)

        self.update_vm_values()

        # Create textbox
        #self.textbox = QLineEdit(self)
        #self.textbox.move(20, 20)
        #self.textbox.resize(280,40)

        # Create a button in the window
        self.but_next = QPushButton('Next Step', self)
        self.but_next.move(110,460)
        self.but_next.clicked.connect(self.next_step_click)

        self.show()

    def update_vm_values(self):
        for i in range(len(self.vm.ram)):
            val = self.ram_vals[i]
            val.setText(bytestr(self.vm.ram[i]))

        for i in range(len(self.vm.rom)):
            romlbl = self.rom_lbls[i]
            if i == self.vm.program_count:
                romlbl.setText(bytestr(i) + ":>")
            else:
                romlbl.setText(bytestr(i) + ":")

        self.acc_val.setText(bytestr(self.vm.accumulator))
        self.pc_val.setText(bytestr(self.vm.program_count))


    @pyqtSlot()
    def next_step_click(self):
        self.vm.next_step()
        self.update_vm_values()

if __name__ == '__main__':
    program = readbin(sys.argv[1])
    #program = [8, 0, 10, 1, 16, 0]
    app = QApplication(sys.argv)
    ex = App(10, program)
    sys.exit(app.exec_())
