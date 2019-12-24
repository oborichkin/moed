import math
import wave
import random
import struct
from collections import OrderedDict

import matplotlib.pyplot as plt
import numpy as np

struct_map = {
    1: 'b',
    2: 'h',
    4: 'i',
    8: 'q'
}


class Model:

    @staticmethod
    def linear(range_, a=1, b=0):
        return Sequence.from_func(range_, lambda x: a*x + b)

    @staticmethod
    def exponential(range_, alpha=1, beta=1):
        return Sequence.from_func(range_, lambda x: beta * math.e ** (alpha * x))

    @staticmethod
    def harmonic(range_, amp=1, freq=1, phase=0, noise_intensity=0):
        return Sequence.from_func(range_, lambda x: math.sin(2 * math.pi * x * freq + phase + random.random() * noise_intensity - noise_intensity / 2) * amp)


class Sequence:

    def __init__(self):
        self._seq = OrderedDict()

    def plot(self):
        plt.figure(figsize=(15, 5))
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

    def __len__(self):
        return len(self._seq)

    def __add__(self, other):
        res = Sequence()
        keys = list(set(self.x).union(other.x))
        keys.sort()
        for x in keys:
            res._seq[x] = 0
            if x in self._seq:
                res._seq[x] += self._seq[x]
            if x in other._seq:
                res._seq[x] += other._seq[x]
        return res

    def __mul__(self, other):
        if isinstance(other, Sequence):
            res = Sequence()
            keys = list(set(self.x).intersection(other.x))
            keys.sort()
            for x in keys:
                res._seq[x] += self._seq[x] * other._seq[x]
            return res
        elif isinstance(other, float) or isinstance(other, int):
            res = Sequence()
            keys = self.x
            for x in keys:
                res._seq[x] = self._seq[x] * other
            return res

    def __sub__(self, other):
        if isinstance(other, int) or isinstance(other, float):
            return Sequence().from_func(self.x, lambda x: self._seq[x] - other)
        if isinstance(other, Sequence):
            return Sequence.from_func(self.x, lambda x: self._seq[x] - other._seq[x])
        else:
            raise ValueError("Operand of this types is not supported")

    def __truediv__(self, other):
        return Sequence.from_func(self.x, lambda x: self._seq[x] / other)

    def hamming(self, alpha=0.46):
        size = len(self)
        y = self.y
        return Sequence.from_func(range(size), lambda x: y[x] * (alpha - (1 - alpha) * math.cos(2 * math.pi * x / size)))


class WaveSequence(Sequence):

    def __init__(self):
        super().__init__()
        self.nchannels = None
        self.nframes = None
        self.freq = None
        self.samp_width = None
        self.frames = None
        self.len = None

    def __len__(self):
        return self.len

    @staticmethod
    def from_file(filename):
        res = WaveSequence()
        wav = wave.open(filename, "r")
        res.nchannels = wav.getnchannels()
        res.nframes = wav.getnframes()
        res.freq = wav.getframerate()
        res.samp_width = wav.getsampwidth()
        res.frames = wav.readframes(res.nframes)
        res.len = int(len(res.frames) / res.samp_width)
        res._seq = OrderedDict(
            zip(
                range(res.len),
                struct.unpack(
                    f"<{res.len}{struct_map[res.samp_width]}", res.frames)
            )
        )
        return res

    def to_file(self, filename):
        res = wave.open(filename, "w")
        res.setnchannels(self.nchannels)
        res.setsampwidth(self.samp_width)
        res.setframerate(self.freq)

        # FIXME add clamp
        data = tuple([x for x in self.y])
        data = struct.pack(f'<{self.len}{struct_map[self.samp_width]}', *data)
        res.writeframesraw(bytes(data))
        res.close()
