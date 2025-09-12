from migen import *
from migen.sim import run_simulation

class ConcatSlice(Module):
    def __init__(self):
        # Entradas
        self.a = Signal(4)
        self.b = Signal(4)
        
        # Salidas
        self.concat = Signal(8)
        self.high = Signal(4)
        self.low = Signal(4)
        self.middle = Signal(4)
        
        # Concatenación
        self.comb += self.concat.eq(Cat(self.a, self.b))
        
        # Slicing
        self.comb += [
            self.high.eq(self.concat[4:8]),    # bits 7-4
            self.low.eq(self.concat[0:4]),     # bits 3-0  
            self.middle.eq(self.concat[2:6])   # bits 5-2
        ]

def concat_slice_test(dut):
    test_cases = [(0x3, 0x5), (0xA, 0xF), (0x7, 0x2)]
    
    for a_val, b_val in test_cases:
        yield dut.a.eq(a_val)
        yield dut.b.eq(b_val)
        yield
        
        concat = yield dut.concat
        high = yield dut.high
        low = yield dut.low
        middle = yield dut.middle
        
        print(f"a=0x{a_val:X}, b=0x{b_val:X}")
        print(f"  concat=0x{concat:02X}, high=0x{high:X}, low=0x{low:X}, middle=0x{middle:X}")

if __name__ == "__main__":
    # Simulación
    dut = ConcatSlice()
    run_simulation(dut, concat_slice_test(dut), vcd_name="concat_slice.vcd")
