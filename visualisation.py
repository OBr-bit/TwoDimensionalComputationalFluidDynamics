import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
class Visualisation:
    def __init__(self) -> None:
        plt.ion()
        self.fig, axes = plt.subplots(2, 2)
        self.flow, self.pressure, self.conflow, self.vorticity = axes.flatten()
        plt.show(block=False)
        
    def Visualise(self, grid, steps):
        self.flow.clear()
        self.pressure.clear()
        self.conflow.clear()
        self.vorticity.clear()
        self.flow.set_title(f"Step {steps}")
        self.flow.quiver(grid.xv, grid.yv, grid.u, grid.v)
        self.pressure.contourf(grid.xv, grid.yv, grid.p)
        self.conflow.streamplot(grid.xv[0, :], grid.yv[:, 0], grid.u, grid.v)
        self.vorticity.contourf(grid.xv, grid.yv, grid.vorticity)
        plt.pause(0.001)
    def SavePlot(self):
        plt.savefig('cfd.Re_10.png', dpi=150,bbox_inches='tight')

if __name__ == "__main__":
    visual = Visualisation()
    grid = Grid(0.1, 0, 1, 0, 1)
    visual.Visualise(grid, 0)