from migen import *
from migen.sim import run_simulation
from migen.fhdl import verilog
import argparse

class Counter(Module):
    def __init__(self):
        # 4 bits → 0..15
        self.count = Signal(4, reset=0)

        # Lógica secuencial: count <= count + 1 en cada ciclo de clk
        self.sync += self.count.eq(self.count + 1)


def counter_test(dut):
    for i in range(20):
        val = (yield dut.count)
        print(f"cycle {i:02d}: count={val}")
        yield


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Counter example with Migen")

    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "-s", "--sim",
        action="store_true",
        help="Run simulation (default if no option is given)"
    )
    group.add_argument(
        "-v", "--verilog",
        action="store_true",
        help="Generate Verilog instead of simulating"
    )

    args = parser.parse_args()
    dut = Counter()

    # Default → simular
    if args.verilog:
        v = verilog.convert(dut, {dut.count})
        print(v)
    else:
        run_simulation(dut, counter_test(dut), vcd_name="counter.vcd")
