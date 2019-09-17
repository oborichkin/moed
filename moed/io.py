class IO:

    @staticmethod
    def normalize(points, s=1):
        x_max = max(points)
        x_min = min(points)
        return [((x - x_min)/(x_max - x_min) - 0.5) * 2 * s
                for x in points]
