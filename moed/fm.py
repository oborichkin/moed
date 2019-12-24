
import math
import random
from collections import OrderedDict
from copy import deepcopy
from typing import List

import matplotlib.pyplot as plt
import numpy as np

from .model import Sequence, Model


class FM(Sequence):

    def __init__(self,
                 signal: Sequence,
                 sampling_period: float,
                 carrier_freq: float = 100,
                 mod: float = 1.0,
                 noise_intensity: float = 0):

        super().__init__()
        self._ts = np.arange(0, 1, sampling_period)

        self._sampling_period = sampling_period
        self._carrier_freq = carrier_freq
        self._carrier_period = 1 / carrier_freq
        self._mod = mod

        self.carrier = Model.harmonic(signal.x, freq=self._carrier_freq)
        self.signal = deepcopy(signal)

        theta = [2 * math.pi * (self._carrier_freq + self._mod * y)
                 * x + random.random() * noise_intensity - noise_intensity / 2 for x, y in signal._seq.items()]
        self.theta = Sequence.from_dict(OrderedDict(zip(signal.x, theta)))

        for x, y in self.theta._seq.items():
            self._seq[x] = math.sin(y)

        self.de_theta = None
        self.demodulated = None
        self.demod()
    
    def demod(self):
        for x, y in self.theta._seq.items():
            self._seq[x] = math.sin(y)
        self.de_theta = Sequence.from_func(
            self.x, lambda x: math.asin(self._seq[x]))
        N = self._carrier_period / self._sampling_period
        Nq = int(N / 4)
        cycles = int(len(self._ts) / N)

        c = []
        for i in range(cycles):
            c.extend([i*4 + 0]*Nq)
            c.extend([i*4 + 1]*Nq)
            c.extend([i*4 + 2]*Nq)
            c.extend([i*4 + 3]*Nq)
        
        res = []
        th = self.de_theta.y
        for i, x in enumerate(c):
            m = x // 4
            r = x % 4
            if r == 0:
                res.append(math.pi * (2 * m + 0)+th[i])
            elif r in [1, 2]:
                res.append(math.pi * (2 * m + 1)-th[i])
            else:
                res.append(math.pi * (2 * m + 2)+th[i])

        res = [th/(2*math.pi * self._ts[i]*self._mod) - self._carrier_freq/self._mod for i, th in enumerate(res)]
        self.demodulated = Sequence.from_dict(OrderedDict(zip(self._ts, res)))

    def plot(self):
        plt.figure(figsize=(15, 5))
        plt.plot(self.x, self.y)
        self.carrier.plot()
        self.signal.plot()
        self.theta.plot()
        self.de_theta.plot()
        self.demodulated.plot()
        plt.show()
