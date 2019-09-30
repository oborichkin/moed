import time
import copy

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

# if __name__ == "__main__":
#     import random
#     r = 1000
#     first = [random.randint(0,1) for x in range(r)]
#     second = [Proc._random2() for x in range(r)]
#     print(first.count(1))
#     print(second.count(1))