from moed.model import Sequence


class Analysis:

    @staticmethod
    def average(sequences):
        res = Sequence()
        for x in sequences[0].x:
            res._seq[x] = 0
            for seq in sequences:
                res._seq[x] += seq._seq[x]
            res._seq[x] /= len(sequences)
        return res