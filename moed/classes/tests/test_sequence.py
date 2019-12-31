import unittest
from moed.classes.sequence import Sequence

x = [x for x in range(1, 11)]
xx = [xx**2 for xx in x]
y = [y for y in range(11, 21)]
d = dict(zip(x,y))


class TestSequenceInitialization(unittest.TestCase):

    def test_basic_init(self):
        seq = Sequence(x, y)
        self.assertListEqual(x, seq.x)
        self.assertListEqual(y, seq.y)

    def test_init_from_dict(self):
        seq = Sequence.from_dict(d)
        self.assertListEqual(x, seq.x)
        self.assertListEqual(y, seq.y)

    def test_init_from_func(self):
        seq = Sequence.from_func(x, lambda x: x**2)
        self.assertListEqual(x, seq.x)
        self.assertListEqual(xx, seq.y)
        