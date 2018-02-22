
# Human Resource Machine VM
A VM for Human Resource Machine with some small modifications compared to
the original game.

- **master:** [![Build Status](https://travis-ci.org/Turysaz/hrmvm.svg?branch=master)](https://travis-ci.org/Turysaz/hrmvm)  
- **dev:** [![Build Status](https://travis-ci.org/Turysaz/hrmvm.svg?branch=dev)](https://travis-ci.org/Turysaz/hrmvm)  

## How to use it
1. Write some HRM assembler code (see specs in `./doc/datasheet.ods`)
2. Assemble using `./hrmasm.sh` (you may use the `-h`)
3. Start either the GUI with `./hrmgui.sh out.hrmbin` or `./hrmterm.sh out.hrmbin`

## Modifications
I did some modifications to the original HRM game. These modifications are:

* Add `LOAD` instruction to load a literal to the accumulator
* Add `NOP` instruction to wait a cycle doing nothing
* There is no `None` value for the accumulator. If an `OUTBOX` operation is
  performed, the accumulator is set to `0` instead.
* No support for letters. **Numeric values only.**
