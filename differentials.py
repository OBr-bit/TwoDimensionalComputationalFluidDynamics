import math

class Differentials:
    def backwardDifference(self, f_x_minus_h, f_x, h):
        return (f_x - f_x_minus_h) / h

    def forwardDifference(self, f_x_plus_h, f_x, h):
        return (f_x_plus_h - f_x) / h

    def centralDifference(self, f_x_plus_h, f_x, f_x_minus_h, h):
        return (f_x_plus_h - 2 * f_x + f_x_minus_h) / math.pow(h, 2)

    def centralDifferenceFirst(self, f_x_plus_h, f_x_minus_h, h):
        return (f_x_plus_h - f_x_minus_h) / (2 * h)
