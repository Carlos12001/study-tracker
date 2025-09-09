# 📘 Semana 1 - Investigación LiteX

## ¿Qué es LiteX?

LiteX es un **framework*️⃣ open-source en Python** para crear **SoCs*️⃣ sobre FPGAs** de forma modular.  
En vez de diseñar todo en Verilog/VHDL, ofrece bloques listos para conectar, simular y generar un sistema.



<small> 🔹 SoC: chip que integra CPU + memoria + periféricos.*  
🔹 *Framework: como un kit de LEGO con piezas listas; en lugar de crear todo desde cero, solo armas con lo que ya viene.*</small>

<p align="center">
  <img src="https://github.com/Carlos12001/study-tracker/blob/master/assitance/images/image_0001.png" width="500" alt="Ejemplo SoC"/>
</p>


## ⚙️ ¿Cómo funciona LiteX?

LiteX describe hardware usando Python + [Migen](https://m-labs.hk/misc/migen/) *️⃣ y lo convierte en HDL (Verilog/VHDL).  
Luego se sintetiza con herramientas open-source o propietarias, generando el *bitstream* para cargar en la FPGA.

<small>🔹 *Migen: librería de Python para describir circuitos digitales de forma más sencilla que en Verilog/VHDL.*</small>


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

<small>🔹 *Verilator: simulador rápido de diseños en Verilog, convierte el hardware en un modelo en C++ para probarlo sin FPGA.*</small>


## 🎯 ¿Para qué se usa?

- Crear SoCs rápidos y flexibles sobre FPGA.  
- Integrar periféricos complejos (PCIe, Ethernet, DRAM, SATA…).  
- Experimentar con CPUs RISC-V y correr sistemas operativos (ej. Linux).  
- Simular diseños completos sin hardware físico.  
- Reutilizar cores ya probados en lugar de empezar desde cero.
