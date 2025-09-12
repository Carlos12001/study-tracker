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

### Ejemplo 1: Toggle simple

```python
from migen import *

class MyToggle(Module):
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
    dut = MyToggle()
    v = verilog.convert(dut, {dut.o})
    print(v)
```

### Ejemplo 2: Blinker (LED parpadeante)

```python
from migen import *
from migen.sim import run_simulation

class Blinker(Module):
    def __init__(self, sys_clk_freq, period):
        self.led = led = Signal()
        toggle = Signal()
        counter_preload = int(sys_clk_freq * period / 2)
        counter = Signal(max=counter_preload + 1)

        self.comb += toggle.eq(counter == 0)
        self.sync += If(toggle,
                        led.eq(~led),
                        counter.eq(counter_preload)
                    ).Else(
                        counter.eq(counter - 1)
                    )

def tb(dut):
    for i in range(25):
        yield
        print(f"cycle {i:02d}: led={(yield dut.led)}")

if __name__ == "__main__":
    blinker = Blinker(sys_clk_freq=100e6, period=1e-1)
    run_simulation(blinker, tb(blinker))
```

> [!NOTE]  
> Este ejemplo sólo se **simula**.  
> El log muestra ciclos y el estado del LED.

### Ejemplo 3: Counter (contador con testbench)

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

    # Opción 1: Simulación
    run_simulation(dut, counter_test(dut), vcd_name="counter.vcd")

    # Opción 2: Generación de Verilog
    dut = Counter()   # reinstanciar antes de convertir
    v = verilog.convert(dut, {dut.count})
    print(v)
```

> [!WARNING]  
> No se puede usar `run_simulation` y `verilog.convert` en la misma ejecución.  
> Una vez simulado un módulo, hay que **reinstanciarlo** si se quiere generar Verilog.
