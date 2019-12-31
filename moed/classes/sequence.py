import numpy as np


class Sequence:

    def __init__(self, x, y):
        # TODO почитать про assert
        assert len(x) == len(y)
        # FIXME стоит ли переезжать на array или np.ndarray?
        self._x = x
        self._y = y

    # TODO а надо ли тогда вообще приватить _x? Зочем нам @property
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    @staticmethod
    def from_dict(d):
        return Sequence(list(d.keys()), list(d.values()))

    @staticmethod
    def from_func(range_, func):
        y = list([func(x) for x in range_])
        return Sequence(list(range_), y)

    def __len__(self):
        return len(self._y)

    def __add__(self, other):
        if isinstance(other, Sequence):
            assert len(self) == len(other)
            y = list([y1 + y2 for y1, y2 in zip(self.y, other.y)])
            # FIXME x передастся по ссылке и пипец!!!
            return Sequence(self.x, y)
        if isinstance(other, list):
            assert len(self) == len(other)
            y = list([y1 + y2 for y1, y2 in zip(self.y, y)])
            # FIXME x передастся по ссылке и пипец!!!
            return Sequence(self.x, y)
        if isinstance(other, (int, float)):
            y = list([y + other for y in self.y])
            # FIXME x передастся по ссылке и пипец!!!
            return Sequence(self.x, y)
        raise NotImplementedError