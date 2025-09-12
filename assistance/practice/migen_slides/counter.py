from migen import *
from migen.sim import run_simulation
from migen.fhdl import verilog

class Counter(Module):
    def __init__(self):
        self.count = Signal(4, reset=0)
        self.sync += self.count.eq(self.count + 1)

def counter_test(dut):
    for i in range(20):
        val = (yield dut.count)
        print(f"cycle {i:02d}: count={val}")
        yield

if __name__ == "__main__":
    dut = Counter()

    # Simulación
    run_simulation(dut, counter_test(dut), vcd_name="counter.vcd")

    # Generación de Verilog
    dut = Counter()   # reinstanciar antes de convertir
    v = verilog.convert(dut, {dut.count})
    print(v)