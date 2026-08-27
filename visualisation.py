import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
class Visualisation:
    def __init__(self) -> None:
        plt.ion()
        self.fig, (self.flow, self.pressure) = plt.subplots(2,1)
        
    def Visualise(self, grid):
        self.flow.clear()
        self.pressure.clear()
        self.flow.quiver(grid.xv, grid.yv, grid.u, grid.v)
        self.pressure.contourf(grid.xv, grid.yv, grid.p)
        plt.pause(0.01)


if __name__ == "__main__":
    visual = Visualisation()
    grid = Grid(0.1, 0, 1, 0, 1)
    visual.Visualise(grid)