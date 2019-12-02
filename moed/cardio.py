import math

from moed.model import Sequence
from moed.analysis import Analysis


class Cardiogram:

    def __init__(self, dots, freq, dt, interval, relaxation):
        self.line = Cardiogram.base(dots, freq, dt, relaxation)
        self.delta = Cardiogram.delta(dots, interval)
        self.gram = Analysis.convolution(self.line, self.delta)
    
    def plot(self):
        self.line.plot()
        self.delta.plot()
        self.gram.plot()

    @staticmethod
    def base(dots, freq, dt, relaxation):
        mult = 2 * math.pi * freq * dt
        return Sequence.from_func(
            range(dots),
            lambda x: math.sin(mult * x) * math.exp(-relaxation * dt * x)
        )

    @staticmethod
    def delta(dots, interval):
        return Sequence.from_func(
            range(dots),
            lambda x: 1 if x % interval == 0 else 0
        )