from migen import *
from migen.fhdl import verilog


class Blinker(Module):
    def __init__(self, sys_clk_freq, period):
        # Señal de salida (equivalente a "output reg led;" en Verilog/SystemVerilog)
        self.led = led = Signal()

        # Señal interna que indica cuándo hay que cambiar el LED
        toggle = Signal()

        # Calculamos el valor máximo del contador:
        counter_preload = int(sys_clk_freq * period / 2)

        # reg [22:0] counter = 23'd5000000; // contador hasta 5e6
        counter = Signal(max=counter_preload + 1)

        # Combinational logic
        self.comb += toggle.eq(counter == 0)

        # Sequential logic
        self.sync += If(toggle,
                        led.eq(~led),                 # led <= ~led;
                        counter.eq(counter_preload)   # counter <= counter_preload;
                    ).Else(
                        counter.eq(counter - 1)       # counter <= counter - 1;
                    )




if __name__=='__main__':

  # Creamos un blinker de 10Hz con un reloj de 100 MHz
  # Equivalente a: un LED que parpadea 10 veces por segundo
  blinker = Blinker(sys_clk_freq=100e6, period=1e-1)

  # Generamos código Verilog del diseño.
  # {blinker.led} especifica qué señales queremos exportar como puertos.
  print(verilog.convert(blinker, {blinker.led}))