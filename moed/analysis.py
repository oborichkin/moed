import math
import statistics
from collections import OrderedDict

from moed.model import Sequence


class Analysis:

    @staticmethod
    def avg(seq, start=0, end=None):
        return sum(seq.y[start:end]) / len(seq.y[start:end])
    
    @staticmethod
    def var(seq, start=0, end=None):
        avg = Analysis.avg(seq, start=start, end=end)
        return sum([(y - avg) ** 2 for y in seq.y])

    @staticmethod
    def average_sequence(sequences):
        res = Sequence()
        for x in sequences[0].x:
            res._seq[x] = 0
            for seq in sequences:
                res._seq[x] += seq._seq[x]
            res._seq[x] /= len(sequences)
        return res
    
    @staticmethod
    def auto_correlation(seq, start=0, end=None):
        avg = Analysis.avg(seq, start=start, end=end)
        var = Analysis.var(seq, start=start, end=end)
        res = OrderedDict()
        if not end:
            end = len(seq._seq)
        for shift in range(start, end):
            res[shift - start] = sum(
                [
                    (seq.y[x] - avg) * (seq.y[x + shift] - avg)
                    for x in range(0, end - shift)
                ]
            ) / var
        return Sequence.from_dict(OrderedDict(zip(seq.x[start:end], res.values())))
    
    @staticmethod
    def cross_correlation(first, second):
        if(len(first) != len(second)):
            raise ValueError("Sequences are not the same size")
        first_avg = Analysis.avg(first)
        second_avg = Analysis.avg(second)
        div = math.sqrt(Analysis.var(first) + Analysis.var(second))

        res = []
        for shift in range(len(first)):
            res.append(
                sum([   
                    (first.y[k] - first_avg) * (second.y[k + shift] - second_avg)
                    for k in range(len(first) - shift)
                ]
            ) / div
        )
        return Sequence.from_dict(OrderedDict(zip(first.x, res)))
    
    @staticmethod
    def dtf(seq):
        n = len(seq)
        res = []
        for k in range(n):
            Re = 0
            Im = 0
            for t in range(n):
                angle = 2 * math.pi * t * k / n
                Re += seq.y[t] * math.cos(angle)
                Im += seq.y[t] * math.sin(angle)
            res.append(math.sqrt(Re ** 2 + Im ** 2))
        return Sequence.from_dict(OrderedDict(zip(seq.x, res)))