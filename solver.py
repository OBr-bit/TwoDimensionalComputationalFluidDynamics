import numpy as np 
import math
from grid import Grid
class Solver:
    def PoissonSolver(self, p, f, h, tolerance, maxRuns):
        before = np.zeros_like(p)
        runs = 0
        while True:
            before = np.copy(p)
            for i in range(1, p.shape[0] - 1, 1):
                for j in range(1, p.shape[1] - 1, 1):
                    p[i,j] = (p[i+1, j] + p[i-1,j] + p[i, j+1] + p[i,j-1] - math.pow(h, 2) * f[i,j]) / 4
            print (p)

            runs = runs + 1
            if (np.max(np.abs(p - before)) <= tolerance or runs > maxRuns):
                break
            
        return p

grid = Grid(0.1, 0, 1, 0, 1)
Solver().PoissonSolver(grid.p, np.zeros(grid.p.shape), grid.h, 0.1, 100)