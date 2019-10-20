import math
from collections import OrderedDict

import matplotlib.pyplot as plt


class Model:

    @staticmethod
    def linear(range_, a=1, b=0):
        return Sequence.from_func(range_, lambda x: a*x + b)

    @staticmethod
    def exponential(range_, alpha=1, beta=1):
        return Sequence.from_func(range_, lambda x: beta * math.e ** (alpha * x))


class Sequence:

    def __init__(self):
        self._seq = OrderedDict()
    
    def plot(self):
        plt.plot(self.x, self.y)
        plt.show()
    
    @property
    def x(self):
        return list(self._seq.keys())
    
    @property
    def y(self):
        return list(self._seq.values())

    @staticmethod
    def from_func(x_range, f):
        res = Sequence()
        for x in x_range:
            res._seq[x] = f(x)
        return res

    @staticmethod
    def from_dict(ordered_dict):
        if isinstance(ordered_dict, OrderedDict):
            res = Sequence()
            res._seq = ordered_dict.copy()
            return res
        raise ValueError("Dictionary must be OrderedDict")

    def __add__(self, other):
        res = Sequence()
        keys = set(self.x).union(other.x)
        for x in keys:
            res._seq[x] = 0
            if x in self.x:
                res._seq[x] += self._seq[x]
            if x in other.x:
                res._seq[x] += other._seq[x]
        return res
    
    def __mul__(self, other):
        res = Sequence()
        keys = set(self.x).union(other.x)
        for x in keys:
            res._seq[x] = 1
            if x in self.x:
                res._seq[x] *= self._seq[x]
            if x in other.x:
                res._seq[x] *= other._seq[x]
        return res
