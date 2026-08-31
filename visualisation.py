from matplotlib.lines import lineStyles
import numpy as np
import matplotlib.pyplot as plt
from grid import Grid
class Visualisation:
    def __init__(self, grid) -> None:
        plt.ion()
        self.fig = plt.figure(figsize=(10, 8))
        plt.show(block=False)

    def Visualise(self, grid, steps):
        self.fig.clear()
        flow = self.fig.add_subplot(3, 2, 1)
        pressure = self.fig.add_subplot(3, 2, 2)
        conflow = self.fig.add_subplot(3, 2, 3)
        vorticity = self.fig.add_subplot(3, 2, 4)
        velocity_profile = self.fig.add_subplot(3,2,5)
        flow.set_title(f"Step {steps}")
        flow.quiver(grid.xv, grid.yv, grid.u, grid.v)
        conflow.streamplot(grid.xv[0, :], grid.yv[:, 0], grid.u, grid.v)
        pressure_plot = pressure.contourf(grid.xv, grid.yv, grid.p)
        vorticity_plot = vorticity.contourf(grid.xv, grid.yv, grid.vorticity)
        velocity_profile.plot(grid.u[:,int(grid.u.shape[1] / 2)], grid.yv[:, 0])
        velocity_profile.axvline(x=0, color='grey', linestyle='--')
        velocity_profile.set_xlabel('u velocity')
        velocity_profile.set_ylabel('y')
        self.fig.colorbar(pressure_plot, ax=pressure)
        self.fig.colorbar(vorticity_plot, ax=vorticity)
        self.fig.tight_layout()
        plt.pause(0.001)
    def SavePlot(self):
        plt.savefig('cfd.Re_10.png', dpi=150,bbox_inches='tight')

if __name__ == "__main__":
    grid = Grid(0.1, 0, 1, 0, 1)
    visual = Visualisation(grid)
    visual.Visualise(grid, 0)