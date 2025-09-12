from migen import *
from migen.sim import run_simulation

class SimpleMemory(Module):
    def __init__(self):
        # Entradas
        self.addr = Signal(2)
        self.data_in = Signal(8)
        self.we = Signal()
        
        # Salida
        self.data_out = Signal(8)
        
        # Memoria: 8 bits x 4 palabras
        mem = Memory(8, 4)
        read_port = mem.get_port()
        write_port = mem.get_port(write_capable=True)
        self.specials += mem, read_port, write_port
        
        # Conexiones
        self.comb += [
            # Puerto de lectura
            read_port.adr.eq(self.addr),
            self.data_out.eq(read_port.dat_r),
            
            # Puerto de escritura
            write_port.adr.eq(self.addr),
            write_port.dat_w.eq(self.data_in),
            write_port.we.eq(self.we)
        ]

def memory_test(dut):
    # Escribir datos
    test_data = [0xAA, 0xBB, 0xCC, 0xDD]
    
    print("Escribiendo datos:")
    for addr, data in enumerate(test_data):
        yield dut.addr.eq(addr)
        yield dut.data_in.eq(data)
        yield dut.we.eq(1)
        yield
        print(f"  Dirección {addr}: 0x{data:02X}")
        yield dut.we.eq(0)
        yield
    
    print("\nLeyendo datos:")
    for addr in range(4):
        yield dut.addr.eq(addr)
        yield
        data = yield dut.data_out
        print(f"  Dirección {addr}: 0x{data:02X}")

if __name__ == "__main__":
    # Simulación
    dut = SimpleMemory()
    run_simulation(dut, memory_test(dut), vcd_name="simple_memory.vcd")