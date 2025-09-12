from migen import *
from migen.fhdl import verilog

class Toggle(Module):
    def __init__(self):
        self.o = Signal()   # salida visible
        d = Signal()
        q = Signal()

        self.comb += [
            self.o.eq(q),
            d.eq(~q)
        ]
        self.sync += q.eq(d)

if __name__ == "__main__":
    dut = Toggle()
    v = verilog.convert(dut, {dut.o})
    print(v)