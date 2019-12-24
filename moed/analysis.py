import math
import statistics
import numpy as np
from collections import OrderedDict

from moed.model import Sequence


class Analysis:

    @staticmethod
    def static_moment(seq, order, start=0, end=None):
        avg = Analysis.avg(seq, start=start, end=end)
        return sum([math.pow(y - avg, order) for y in seq.y[start:end]]) / len(seq.y[start:end])

    @staticmethod
    def avg(seq, start=0, end=None):
        return sum(seq.y[start:end]) / len(seq.y[start:end])
    
    @staticmethod
    def var(seq, start=0, end=None):
        return Analysis.static_moment(seq, 2, start, end)
    
    @staticmethod
    def skewness(seq, start=0, end=None):
        return Analysis.static_moment(seq, 3, start, end)

    @staticmethod
    def excess(seq, start=0, end=None):
        return Analysis.static_moment(seq, 4, start, end)
    
    @staticmethod
    def stdev(seq, start=0, end=None):
        return math.sqrt(Analysis.var(seq, start, end))
    
    @staticmethod
    def amp(seq, start=0, end=None):
        return max(seq.y[start:end]) - min(seq.y[start:end])
    
    @staticmethod
    def MS(seq, start=0, end=None):
        return sum([y ** 2 for y in seq.y[start:end]]) / len(seq.y[start:end])
    
    @staticmethod
    def MSE(seq, start=0, end=None):
        return math.sqrt(Analysis.MS(seq, start, end))
    
    @staticmethod
    def assymmetry(seq, start=0, end=None):
        skewness = Analysis.skewness(seq, start, end)
        stdev = Analysis.stdev(seq, start, end)
        return (skewness / stdev ** 3)
    
    @staticmethod
    def kurtosis(seq, start=0, end=None):
        var = Analysis.var(seq, start, end)
        ex = Analysis.excess(seq, start, end)
        return (ex / var ** 2) - 3

    @staticmethod
    def std_abs_dev(seq, start=0, end=None):
        avg = Analysis.avg(seq, start, end)
        return sum([abs(y - avg) for y in seq.y[start:end]]) / len(seq.y[start:end])

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
        y = seq.y
        if not end:
            end = len(seq._seq)
        for shift in range(start, end):
            res[shift - start] = sum(
                [
                    (y[x] - avg) * (y[x + shift] - avg)
                    for x in range(0, end - shift)
                ]
            ) / var
        return Sequence.from_dict(OrderedDict(zip(seq.x[start:end], res.values())))
    
    @staticmethod
    def gist(seq, intervals=10):
        from collections import defaultdict
        res = defaultdict(int)
        mi = min(seq.y)
        ma = max(seq.y)
        size = (ma - mi) / intervals
        for y in seq.y:
            idx = (y - mi) // size
            res[idx] += 1
        return Sequence.from_func(range(intervals), lambda x: res[x])
    
    @staticmethod
    def cross_correlation(first, second):
        if(len(first) != len(second)):
            raise ValueError("Sequences are not the same size")
        first_avg = Analysis.avg(first)
        second_avg = Analysis.avg(second)
        div = math.sqrt(Analysis.var(first) + Analysis.var(second))

        res = []
        f_y = first.y
        s_y = second.y
        for shift in range(len(first)):
            res.append(
                sum([   
                    (f_y[k] - first_avg) * (s_y[k + shift] - second_avg)
                    for k in range(len(first) - shift)
                ]
            ) / div
        )
        return Sequence.from_dict(OrderedDict(zip(first.x, res)))
    
    @staticmethod
    def convolution(first, second):
        one = first.y
        two = second.y
        n = len(first)
        m = len(second)
        conv = []
        for i in range(n):
            if i in range(n+m):
                res = 0
                for j in range(m+1):
                    if (i - j) in range(1, n+1):
                        res += one[i - j] * two[j]
                conv.append(res)
            else:
                conv.append(0)
        return Sequence.from_func(range(n), lambda x: conv[x])

    @staticmethod
    def dtf(seq):
        n = len(seq)
        y_tmp = seq.y
        res = []
        for k in range(n):
            Re = 0
            Im = 0
            for t in range(n):
                angle = 2 * math.pi * t * k / n
                Re += y_tmp[t] * math.cos(angle)
                Im += y_tmp[t] * math.sin(angle)
            res.append(math.sqrt((Re / n) ** 2 + (Im / n) ** 2))
        
        return Sequence.from_dict(OrderedDict(zip(seq.x[:n//2:], res[:n//2])))
    
    @staticmethod
    def dft(seq):
        return Analysis.dtf(seq)
    
    @staticmethod
    def fft(seq):
        n = len(seq)
        res = seq.y
        res = np.fft.fft(res)
        res = [abs(x) for x in res]
        return Sequence.from_dict(OrderedDict(zip(seq.x[:n//2], res[:n//2])))
    
    @staticmethod
    def ifft(seq):
        pass
    
    @staticmethod
    def dft_complex(seq):
        res = []
        n = len(seq)
        y = seq.y
        for k in range(n):
            Re = 0
            Im = 0
            for t in range(n):
                angle = 2 * math.pi * t * k / n
                Re += y[t] * math.cos(angle)
                Im += y[t] * math.sin(angle)
            res.append((Re / n, Im / n))
        return res

    @staticmethod
    def idft(seq):
        n = len(seq)
        res = [0] * n
        y = seq.y
        for k in range(n):
            re = 0
            im = 0
            for t in range(n):
                angle = 2 * math.pi * t * k / n
                re += y[t] * math.cos(angle)
                im += y[t] * math.sin(angle)
            res[k] = re + im
        return Sequence.from_func(range(n), lambda x: res[x])

    @staticmethod
    def idft_from_complex(complex_pairs):
        res = []
        n = len(complex_pairs)
        for k in range(n):
            sum = 0
            for t in range(n):
                angle = (2 * math.pi * k * t) / n
                sum += complex_pairs[t][0] * math.cos(angle) + complex_pairs[t][1] * math.sin(angle)
            res.append(sum)
        return Sequence.from_func(range(n), lambda x: res[x])

