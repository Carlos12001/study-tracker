# 📘 Semana 1 - Investigación LiteX

## ¿Qué es LiteX?

LiteX es un **framework*️⃣ open-source en Python** para crear **SoCs*️⃣ sobre FPGAs** de forma modular.  
En vez de diseñar todo en Verilog/VHDL, ofrece bloques listos para conectar, simular y generar un sistema.

<small> 🔹 SoC: chip que integra CPU + memoria + periféricos.
🔹 Framework: como un kit de LEGO con piezas listas; en lugar de crear todo desde cero, solo armas con lo que ya viene.</small>


<p align="center">
  <img src="https://github.com/Carlos12001/study-tracker/blob/master/assitance/images/image_0001.png" width="500" alt="Ejemplo SoC"/>
</p>


## ⚙️ ¿Cómo funciona LiteX?

LiteX describe hardware usando Python + [Migen](https://m-labs.hk/misc/migen/) *️⃣ y lo convierte en HDL (Verilog/VHDL).  
Luego se sintetiza con herramientas open-source o propietarias, generando el *bitstream* para cargar en la FPGA.

<small>🔹 Migen: librería de Python para describir circuitos digitales de forma más sencilla que en Verilog/VHDL.</small>


## 🔄 Flujo de trabajo

```bash
Tu código Python (Migen/LiteX)
         ↓
Generación HDL (Verilog)
         ↓
Síntesis (Vivado/Quartus/nextpnr/Yosys)
         ↓
Bitstream para FPGA
```


## 🧰 Tecnologías que usa

- **Lenguaje base:** Python + Migen  
- **Compatibilidad:** Verilog · VHDL · nMigen · SpinalHDL  
- **Simulación:** [Verilator](https://www.veripool.org/verilator/)*️⃣  
- **Síntesis:** Yosys/nextpnr · Vivado · Quartus  
- **CPUs soportadas:** VexRiscv · Rocket · PicoRV32 · LM32 · BlackParrot  

<small>🔹 Verilator: simulador rápido de diseños en Verilog, convierte el hardware en un modelo en C++ para probarlo sin FPGA.</small>


## 🎯 ¿Para qué se usa?

- Crear SoCs rápidos y flexibles sobre FPGA.  
- Integrar periféricos complejos (PCIe, Ethernet, DRAM, SATA…).  
- Experimentar con CPUs RISC-V y correr sistemas operativos (ej. Linux).  
- Simular diseños completos sin hardware físico.  
- Reutilizar cores ya probados en lugar de empezar desde cero.

## 🧩 Arquitectura de LiteX

LiteX actúa como **pegamento** entre:
- Los **softcores** (CPUs implementadas en lógica programable).  
- Los **periféricos** (Ethernet, DRAM, SATA, PCIe, UART, etc.).  
- El **bus de interconexión** (Wishbone, AXI, Avalon-ST).  

Todo se define en Python, y LiteX se encarga de generar el RTL, la conexión entre bloques y el *CSR map* (registros de control).

## 🖥️ Cores principales

LiteX tiene un ecosistema de módulos reutilizables llamados **LiteX cores**:
- **LiteDRAM:** controlador de memoria SDR/DDR/DDR3.  
- **LiteEth:** Ethernet hasta 1 Gbps.  
- **LitePCIe:** PCIe hasta Gen2 x4.  
- **LiteSATA:** almacenamiento SATA 1/2/3.  
- **LiteScope:** analizador lógico embebido.  
- **LiteSDCard, LiteSPI, LiteUSB, LiteVideo…**  

Esto evita que los estudiantes tengan que programar periféricos desde cero.

## 🧠 Softcores soportados

LiteX soporta varias CPUs “soft” que se implementan dentro de la FPGA:
- **VexRiscv (RISC-V):** flexible, rápido, ideal para correr Linux.  
- **PicoRV32 (RISC-V):** muy pequeño, perfecto para demos educativas.  
- **LM32 (Lattice Micro32):** legado, simple de entender.  
- **Rocket Chip (RISC-V):** núcleo de Berkeley, más avanzado.  
- **BlackParrot (RISC-V multicore).**

<small>🔹 Softcore: procesador implementado en la FPGA por lógica programable, no grabado físicamente como un ARM Cortex en un SoC comercial.</small>

## 🧰 Tecnologías que usa

- **Lenguaje base:** Python + Migen  
- **Compatibilidad:** Verilog · VHDL · nMigen · SpinalHDL  
- **Simulación:** [Verilator](https://www.veripool.org/verilator/) *️⃣  
- **Síntesis:** Yosys/nextpnr · Vivado · Quartus  
- **CPUs soportadas:** VexRiscv · Rocket · PicoRV32 · LM32 · BlackParrot  

<small>🔹 Verilator: simulador rápido de diseños en Verilog, convierte el hardware en un modelo en C++ para probarlo sin FPGA.</small>

## ⚖️ Comparación con Vivado

- **Vivado (Xilinx):**
  - Entorno gráfico, intuitivo para principiantes.  
  - Fuerte dependencia de IPs propietarios.  
  - Menos flexible fuera del ecosistema Xilinx.  

- **LiteX:**
  - Basado en scripts Python → más flexible y portable.  
  - Ecosistema de IPs open-source (DRAM, Ethernet, PCIe, etc.).  
  - Curva de aprendizaje: requiere Linux/terminal.  

## 📝 Notas de instalación

En Ubuntu, la instalación básica es con `apt`:

```bash
sudo apt update
sudo apt install python3 python3-pip git meson ninja-build \
                 libevent-dev libjson-c-dev verilator
```

Después instalar LiteX:

```bash
wget https://raw.githubusercontent.com/enjoy-digital/litex/master/litex_setup.py
chmod +x litex_setup.py
./litex_setup.py --init --install --user
```

Y para probar la simulación:

```bash
litex_sim --cpu-type=vexriscv
```

Si aparece el prompt del BIOS → LiteX está funcionando.

## Implementaciones de SoCs de FPGA 

### Digilent Basys3 

### Terasic DE1-Standard
