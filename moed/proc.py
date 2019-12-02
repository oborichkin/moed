import time
import copy
import math
from collections import OrderedDict

from moed.analysis import Analysis
from moed.model import Sequence


class Filter:

    P310_WINDOW = (0.35577019, 0.24369830, 0.07211497, 0.00630165)

    @staticmethod
    def low_pass_filter(size, dt, fc):
        half = Filter._half_filter(size, dt, fc)
        result = [*list(reversed(half)), *half[1:]]
        return Sequence.from_func(range(2*size+1), lambda x: result[x])

    @staticmethod
    def high_pass_filter(size, dt, fc):
        lpf = Filter.low_pass_filter(size, dt, fc)
        lpw = lpf.y
        hpf = []
        for i in range(2*size+1):
            if i == size:
                hpf.append(1 - lpw[i])
            else:
                hpf.append(-lpw[i])
        return Sequence.from_func(range(2*size+1), lambda x: hpf[x])
    
    @staticmethod
    def band_pass_filter(size, dt, fc_low, fc_up):
        assert fc_low < fc_up
        return Filter._band_filter(size, dt, fc_low, fc_up)
    
    @staticmethod
    def band_select_filter(size, dt, fs_low, fs_up):
        assert fs_low < fs_up
        return Filter._band_filter(size, dt, fs_up, fs_low)

    @staticmethod
    def high_cut_filter(size, dt, fc):
        return Filter.low_pass_filter(size, dt, fc)

    @staticmethod
    def low_cut_filter(size, dt, fc):
        return high_pass_filter(size, dt, fc)

    @staticmethod
    def _band_filter(size, dt, fc1, fc2):
        lpf_low = Filter.low_pass_filter(size, dt, fc1).y
        lpf_up = Filter.low_pass_filter(size, dt, fc2).y

        for i in range(2*size + 1):
            if i == size:
                lpf_low[i] = 1 + lpf_low[i] - lpf_up[i]
            else:
                lpf_low[i] = lpf_low[i] - lpf_up[i]
        return Sequence.from_func(range(2*size+1), lambda x: lpf_low[x])
    
    @staticmethod
    def _half_filter(size, dt, fc):
        lpw = []
        # Straight part
        arg = 2 * fc * dt
        lpw.append(arg)
        arg *= math.pi
        for i in range(1, size+1):
            lpw.append(math.sin(arg * i) / (math.pi * i))
        # Trapezoid
        lpw[size] /= 2
        # Appliement of smoothing window
        sumg = lpw[0]
        for i in range(1, size+1):
            sum_ = Filter.P310_WINDOW[0]
            arg = (math.pi * i) / size
            for k in range(1, 4):
                sum_ +=  2 * Filter.P310_WINDOW[k] * math.cos(arg * k)
            lpw[i] *= sum_
            sumg += lpw[i] * 2
        # Normalization
        for i in range(size+1):
            lpw[i] /= sumg
        
        return lpw


class Proc:

    @staticmethod
    def shift(N, m, n, C):
        return [x+C if idx >= m and idx <=n
                    else x
                    for idx, x in enumerate(N)]
    
    @staticmethod
    def spikes(N, m, S):
        res = copy.copy(N)
        for i in range(m):
            res[int(Proc.my_random(end=len(N)))] *= S
        return res

    @staticmethod
    def unshift(seq):
        res = copy.deepcopy(seq)
        return res - Analysis.avg(res)    

    @staticmethod
    def unspike(seq, clamp):
        res = copy.deepcopy(seq)
        for i in range(1,len(res)-1):
            if abs(res.y[i]) > clamp:
                res._seq[res.x[i]] = (res.y[i-1] + res.y[i+1]) / 2
        return res
    
    @staticmethod
    def untrend(seq, window_size=5):
        res = OrderedDict()
        for idx, x in enumerate(seq.x):
            res[x] = Analysis.avg(seq, max(0, idx-window_size), min(len(seq)-1, idx+window_size))
        return seq - Sequence.from_dict(res)

    @staticmethod
    def my_random(start=0, end=1):
        s = ""
        for x in range(8):
            s += str(Proc._random2())
        return (int(s, 2) / 255) * (end - start) + start

    @staticmethod
    def _random2():
        l = [Proc._random() for x in range(1000)]
        if l.count(1) > l.count(0):
            return 1
        return 0

    @staticmethod
    def _random():
        return int(time.time() * 10000) % 2