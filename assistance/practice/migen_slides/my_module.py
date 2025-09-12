from migen import *

class MyModule(Module):
  def __init__(self):
      self.o = Signal()   # salida

      d = Signal()
      q = Signal()

      # Combinational logic
      self.comb += [
          self.o.eq(q),
          d.eq(~q)
      ]

      # Synchronous logic
      self.sync += q.eq(d)
