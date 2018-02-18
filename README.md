
# Human Resource Machine VM
A VM for Human Resource Machine with some small modifications compared to
the original game.


## Modifications
I did some modifications to the original HRM game. These modifications are:

* Add LOAD instruction to load a literal to the accumulator
* Add NOP instruction to wait a cycle doing nothing
* There is no `None` value for the accumulator. If an `OUTBOX` operation is
  performed, the accumulator is set to `0` instead.
* No support for letters. **Numeric values only.**
