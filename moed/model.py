import math


class Model:

    @staticmethod
    def linear(range_, a=1, b=0):
        return [a*x + b for x in range_]

    @staticmethod
    def exponential(range_, alpha=1, beta=1):
        return [beta * math.e ** (alpha * x) for x in range_]
