# Tutorial de Verilog a Migen

Este documento es una **guía práctica** de Migen la librería de Python.

## 1. Señales básicas

### En Verilog

```verilog
module top(
  input  wire clk,
  input  wire a,
  input  wire b,
  output reg  y
);
  always @(posedge clk) begin
    y <= a & b;
  end
endmodule
```

### En Migen

```python
from migen import *

class Top(Module):
    def __init__(self):
        # señales externas
        self.a = Signal()
        self.b = Signal()
        self.y = Signal()

        self.sync += self.y.eq(self.a & self.b)
```

- **`Signal()`** = equivalente a `reg`/`wire` en Verilog.
- `Module` encapsula el diseño y maneja `comb`, `sync`, `submodules`, etc.

#### Parámetros Opcionales de `Signal`

`Signal()` en Migen puede recibir varios argumentos opcionales:

- **`Signal(nbits)`** → define el ancho en bits (por defecto es 1).  
  Ejemplo:

  ```python
  s = Signal(8)   # señal de 8 bits, unsigned
  ```

- **`Signal((nbits, signed))`** → define ancho y si es con signo.  
  Ejemplo:

  ```python
  s = Signal((8, True))   # señal de 8 bits con signo
  ```

- **`name="foo"`** → sugerencia de nombre en el Verilog generado.  
  Ejemplo:

  ```python
  counter = Signal(8, name="counter")
  ```

- **`reset=value`** → valor inicial al reset o default en lógica combinacional.  
  Ejemplo:

  ```python
  s = Signal(8, reset=5)   # inicia en 5 tras reset
  ```

- **`min= , max=`** → rango numérico, Migen calcula ancho y signo automáticamente.  
  Ejemplo:

  ```python
  s = Signal(min=-8, max=8)   # 4 bits con signo (-8 a 7)
  ```

## 2. Lógica combinacional

### Verilog

```verilog
assign y = a ^ b;
```

### Migen

```python
class CombExample(Module):
    def __init__(self):
        # señales externas
        self.a = Signal()
        self.b = Signal()
        self.y = Signal()

        self.comb += self.y.eq(self.a ^ self.b)
```

## 3. Flip-Flops y registros

### Verilog

```verilog
always @(posedge clk) begin
  q <= d;
end
```

### Migen

```python
class FFExample(Module):
    def __init__(self):
        # señales externas
        self.d = Signal()
        self.q = Signal()

        self.sync += self.q.eq(self.d)
```

## 4. If / Case

### Verilog (if)

```verilog
always @(posedge clk) begin
  if (enable)
    q <= d;
  else
    q <= 0;
end
```

### Migen (If)

```python
class IfExample(Module):
    def __init__(self):
        # señales externas
        self.enable = Signal()
        # señales internas
        self.d = Signal()
        self.q = Signal()

        self.sync += If(self.enable,
            self.q.eq(self.d)
        ).Else(
            self.q.eq(0)
        )
```

---

### Verilog (case)

```verilog
always @(posedge clk) begin
  case(sel)
    2'b00: y <= a;
    2'b01: y <= b;
    2'b10: y <= c;
    default: y <= 0;
  endcase
end
```

### Migen (Case)

```python
class CaseExample(Module):
    def __init__(self):
        # señales externas
        self.sel = Signal(2)
        # señales internas
        self.a   = Signal()
        self.b   = Signal()
        self.c   = Signal()
        self.y   = Signal()

        self.sync += Case(self.sel, {
            0: self.y.eq(self.a),
            1: self.y.eq(self.b),
            2: self.y.eq(self.c),
            "default": self.y.eq(0)
        })
```

## 5. Concatenación y slicing

### Verilog

```verilog
assign y = {a, b};
assign z = x[3:0];
```

### Migen

```python
class SliceExample(Module):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.y = Signal(2)
        self.x = Signal(8)
        self.z = Signal(4)

        self.comb += [
            self.y.eq(Cat(self.a, self.b)),
            self.z.eq(self.x[0:4])  # slices estilo Python
        ]
```

## 6. Arrays

### SystemVerilog

En `Verilog` _no existen arrays dinámicos_; se usan muxes/memoria.

```verilog
module ArrayExample(
    input  logic [1:0] index,
    input  logic       a, b, c, d,
    output logic       y
);
    // Declaramos un arreglo de 4 señales de 1 bit
    logic arr [3:0];

    // Asignamos valores a cada posición
    assign arr[0] = a;
    assign arr[1] = b;
    assign arr[2] = c;
    assign arr[3] = d;

    // Seleccionamos dinámicamente según index
    assign y = arr[index];
endmodule
```

### Migen

```python
class ArrayExample(Module):
    def __init__(self):
        self.index = Signal(2)
        self.y = Signal()
        self.arr = Array(Signal() for _ in range(4))

        self.comb += self.y.eq(self.arr[self.index])
```

## 7. FSM (máquinas de estados)

### Verilog

```verilog
always @(posedge clk) begin
  case (state)
    0: if (start) state <= 1;
    1: if (done)  state <= 2;
    2: state <= 0;
  endcase
end
```

### Migen

```python
from migen.genlib.fsm import FSM, NextState

class FSMExample(Module):
    def __init__(self):
        self.start = Signal()
        self.done = Signal()

        fsm = FSM(reset_state="IDLE")
        self.submodules += fsm

        fsm.act("IDLE",
            If(self.start, NextState("RUN"))
        )
        fsm.act("RUN",
            If(self.done, NextState("END"))
        )
        fsm.act("END",
            NextState("IDLE")
        )
```

## 8. Instanciación de módulos externos

### Verilog

```verilog
my_ip u1 (
  .clk(clk),
  .a(a),
  .y(y)
);
```

### Migen

```python
class InstExample(Module):
    def __init__(self, clk, a, y):
        self.specials += Instance("my_ip",
            clk=clk,
            a=a,
            y=y
        )
```

## 9. Memorias

### Verilog

```verilog
reg [7:0] mem[0:255];
```

### Migen

```python
class MemExample(Module):
    def __init__(self):
        mem = Memory(8, 256)
        port = mem.get_port(write_capable=True)
        self.specials += mem, port
```

## 10. Simulación en Migen

```python
class Top(Module):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.y = Signal()
        self.comb += self.y.eq(self.a & self.b)

def tb(dut):
    yield dut.a.eq(1)
    yield dut.b.eq(0)
    yield
    print((yield dut.y))

dut = Top()
run_simulation(dut, tb(dut), vcd_name="top.vcd")
```

## 11. Conversión a Verilog

```python
from migen.fhdl.verilog import convert

class Top(Module):
    def __init__(self):
        self.a = Signal()
        self.b = Signal()
        self.y = Signal()
        self.comb += self.y.eq(self.a ^ self.b)

dut = Top()
convert(dut, ios={dut.a, dut.b, dut.y}).write("top.v")
```

---

## Ejercicios prácticos

Se le recomienda al usuario intentar primero el ejercicio y luego ver las respuestas.

### Ejemplo 1: Toggle simple

**Especificación:**
Diseña un circuito que cambie su salida en cada ciclo de reloj. La salida debe alternar entre 0 y 1 continuamente, creando un patrón de toggle básico.

- **Entrada:** Ninguna (solo reloj implícito)
- **Salida:** `o` - señal que alterna cada ciclo
- **Comportamiento:** En cada flanco positivo del reloj, la salida debe cambiar de estado

```python
from migen import *
from migen.fhdl import verilog

class Toggle(Module):
    def __init__(self):
        self.o = Signal()   # salida visible
        d = Signal()
        q = Signal()

        self.comb += [
            self.o.eq(q),
            d.eq(~q)
        ]
        self.sync += q.eq(d)

if __name__ == "__main__":
    dut = Toggle()
    v = verilog.convert(dut, {dut.o})
    print(v)
```

```bash
python toggle.py
```

### Ejemplo 2: Counter (contador con testbench)

Implementa un contador de 4 bits que se incrementa en cada ciclo de reloj y se reinicia automáticamente cuando alcanza su valor máximo.

- **Entrada:** Ninguna (solo reloj y reset implícitos)
- **Salida:** `count` - contador de 4 bits (0-15)
- **Comportamiento:**
  - Inicia en 0 después del reset
  - Se incrementa en 1 cada ciclo de reloj
  - Se reinicia automáticamente después de 15 (overflow)

```python
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
```

> [!WARNING]  
> No se puede usar `run_simulation` y `verilog.convert` en la misma ejecución.  
> Una vez simulado un módulo, hay que **reinstanciarlo** si se quiere generar Verilog.

```bash
# Para ejecutar simulación y generar Verilog
python counter.py

gtkwave counter.vcd
```

### Ejercicio 3: Multiplexor con FSM

**Especificación:**
Diseña un multiplexor de 4 entradas controlado por una máquina de estados que rota automáticamente entre las entradas.

- **Entradas:** `a`, `b`, `c`, `d` - 4 señales de 1 bit
- **Salida:** `y` - salida multiplexada
- **Comportamiento:** La FSM rota automáticamente cada ciclo: A → B → C → D → A

```python
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
```

```bash
python mux_fsm.py
gtkwave mux_fsm.vcd
```

### Ejercicio 4: Concatenación y Slicing

**Especificación:**
Diseña un circuito que tome dos señales de 4 bits, las concatene en una de 8 bits, y luego extraiga diferentes partes usando slicing.

- **Entradas:** `a`, `b` - dos señales de 4 bits cada una
- **Salidas:**
  - `concat` - concatenación completa de 8 bits
  - `high` - 4 bits superiores
  - `low` - 4 bits inferiores
  - `middle` - 4 bits del medio (bits 2-5)

```python
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

```

```bash
python concat_slice.py
gtkwave concat_slice.vcd
```

---

### Ejercicio 5: Memoria Simple

**Especificación:**
Implementa una memoria RAM básica de 4 palabras de 8 bits con operaciones simples de lectura y escritura.

- **Entradas:**
  - `addr` - dirección de 2 bits (0-3)
  - `data_in` - datos de entrada de 8 bits
  - `we` - write enable
- **Salida:** `data_out` - datos de salida de 8 bits

```python
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
```

```bash
python simple_memory.py
gtkwave simple_memory.vcd
```
