#!/usr/bin/env python3
# SoC mínimo para Basys-3: CPU RISC-V + BIOS (ROM) + RAM + UART.

from migen import *
from litex.gen import *
from litex.soc.integration.soc_core import SoCCore
from litex.soc.integration.builder  import Builder
from litex.soc.cores.clock import S7PLL                     # PLL p/ Xilinx 7-series

# Plataforma Basys-3 (nombre del módulo puede variar entre instalaciones)
try:
    from litex_boards.platforms import digilent_basys3 as basys3
except ImportError:
    from litex_boards.platforms import basys3 as basys3     # fallback si tu árbol la llama "basys3"

# --- CRG: genera el reloj/reset del dominio 'sys' a partir de clk100 de la board ---
class CRG(Module):
    def __init__(self, platform, sys_clk_freq):
        self.clock_domains.cd_sys = ClockDomain()           # dominio de reloj principal
        clk100 = platform.request("clk100")                 # pin de 100 MHz de la Basys-3
        self.submodules.pll = S7PLL(speedgrade=-1)
        self.pll.register_clkin(clk100, 100e6)              # entrada del PLL a 100 MHz
        self.pll.create_clkout(self.cd_sys, sys_clk_freq)   # salida 'sys' a la freq deseada

# --- SoC: integra CPU + ROM (BIOS) + RAM + UART sobre el bus interno ---
class BaseSoC(SoCCore):
    def __init__(self, sys_clk_freq=int(50e6)):
        platform = basys3.Platform()                        # describe pines/IOs de la board
        SoCCore.__init__(
            self, platform,
            clk_freq                 = sys_clk_freq,        # freq del dominio 'sys'
            integrated_rom_size      = 0x8000,              # 32 KiB BIOS
            integrated_main_ram_size = 0x4000,              # 16 KiB RAM
            cpu_type                 = "vexriscv",          # core RISC-V
            uart_name                = "serial",            # UART por FTDI de la Basys-3
        )
        self.submodules.crg = CRG(platform, sys_clk_freq)   # engancha el CRG

        # (Opcional) ejemplo de LED:
        # led = platform.request("user_led", 0)
        # self.comb += led.eq(0)

def main():
    soc = BaseSoC(sys_clk_freq=int(50e6))                   # 50 MHz para 'sys'
    builder = Builder(soc, output_dir="build/basys3")       # carpeta de salida
    builder.build(run=True)                                 # genera bitstream + BIOS

if __name__ == "__main__":
    main()
