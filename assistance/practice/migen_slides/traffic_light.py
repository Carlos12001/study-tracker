from migen import *
from migen.genlib.fsm import FSM, NextState
from migen.sim import run_simulation

class MuxFSM(Module):
    def __init__(self):
        # Entradas
        self.a = Signal()
        self.b = Signal() 
        self.c = Signal()
        self.d = Signal()
        
        # Salida
        self.y = Signal()
        
        # Máquina de estados
        fsm = FSM(reset_state="SEL_A")
        self.submodules.fsm = fsm
        
        fsm.act("SEL_A",
            self.y.eq(self.a),
            NextState("SEL_B")
        )
        fsm.act("SEL_B", 
            self.y.eq(self.b),
            NextState("SEL_C")
        )
        fsm.act("SEL_C",
            self.y.eq(self.c),
            NextState("SEL_D")
        )
        fsm.act("SEL_D",
            self.y.eq(self.d),
            NextState("SEL_A")
        )

def mux_fsm_test(dut):
    # Establecer valores de entrada
    yield dut.a.eq(1)
    yield dut.b.eq(0)
    yield dut.c.eq(1)
    yield dut.d.eq(0)
    yield
    
    for i in range(8):
        output = yield dut.y
        print(f"cycle {i:02d}: output={output}")
        yield

if __name__ == "__main__":
    # Simulación
    dut = MuxFSM()
    run_simulation(dut, mux_fsm_test(dut), vcd_name="mux_fsm.vcd")