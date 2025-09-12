from migen import *
from migen.genlib.fsm import FSM, NextState
from migen.sim import run_simulation

class TrafficLight(Module):
    def __init__(self):
        # Salidas
        self.red = Signal()
        self.yellow = Signal()
        self.green = Signal()
        
        # Máquina de estados
        fsm = FSM(reset_state="GREEN")
        self.submodules.fsm = fsm
        
        fsm.act("GREEN",
            self.green.eq(1),
            self.yellow.eq(0),
            self.red.eq(0),
            NextState("YELLOW")
        )
        fsm.act("YELLOW",
            self.green.eq(0),
            self.yellow.eq(1),
            self.red.eq(0),
            NextState("RED")
        )
        fsm.act("RED",
            self.green.eq(0),
            self.yellow.eq(0),
            self.red.eq(1),
            NextState("GREEN")
        )

def traffic_light_test(dut):
    for i in range(12):
        red = yield dut.red
        yellow = yield dut.yellow
        green = yield dut.green
        
        # Mostrar qué luz está encendida
        light = "GREEN" if green else ("YELLOW" if yellow else "RED")
        print(f"cycle {i:02d}: {light} (R={red} Y={yellow} G={green})")
        yield

if __name__ == "__main__":
    # Simulación
    dut = TrafficLight()
    run_simulation(dut, traffic_light_test(dut), vcd_name="traffic_light.vcd")
