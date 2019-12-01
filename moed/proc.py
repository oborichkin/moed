import time
import copy
from collections import OrderedDict

from moed.analysis import Analysis
from moed.model import Sequence


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