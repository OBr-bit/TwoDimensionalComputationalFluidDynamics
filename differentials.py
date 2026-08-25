class Differentials:
    def backwardDifference(self, left, x, h):
        return (x - left) / h
    def forwardDifference(self, right, x, h):
        return (right - x) / h
        