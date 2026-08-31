import matplotlib.pyplot as plt
from grid import Grid

class Visualisation:
    def __init__(self, grid, h, nu, timestep, rho, u, L) -> None:
        plt.ion()
        self.fig = plt.figure(figsize=(10, 8))
        plt.show(block=False)
        self.h = h
        self.nu = nu
        self.timestep = timestep
        self.rho = rho
        self.RE = (u * L)/self.nu

    def Visualise(self, grid, steps, convergence):
        self.fig.clear()

        flow = self.fig.add_subplot(3, 2, 1)
        flow.set_title("Velocity Field")
        flow.set_xlabel("x")
        flow.set_ylabel("y")
        flow.quiver(grid.xv, grid.yv, grid.u, grid.v)

        pressure = self.fig.add_subplot(3, 2, 2)
        pressure.set_title("Pressure")
        pressure.set_xlabel("x")
        pressure.set_ylabel("y")
        pressure_plot = pressure.contourf(grid.xv, grid.yv, grid.p)

        conflow = self.fig.add_subplot(3, 2, 3)
        conflow.set_title("Streamlines")
        conflow.set_xlabel("x")
        conflow.set_ylabel("y")
        conflow.streamplot(grid.xv[0, :], grid.yv[:, 0], grid.u, grid.v)

        vorticity = self.fig.add_subplot(3, 2, 4)
        vorticity.set_title("Vorticity")
        vorticity.set_xlabel("x")
        vorticity.set_ylabel("y")
        vorticity_plot = vorticity.contourf(grid.xv, grid.yv, grid.vorticity)

        velocity_profile = self.fig.add_subplot(3, 2, 5)
        velocity_profile.set_title("Velocity Profile (mid-slice)")
        velocity_profile.set_xlabel('u velocity')
        velocity_profile.set_ylabel('y')
        velocity_profile.plot(grid.u[:,int(grid.u.shape[1] / 2)], grid.yv[:, 0])
        velocity_profile.axvline(x=0, color='grey', linestyle='--')

        params_details = self.fig.add_subplot(3, 2, 6)
        params_details.axis('off')
        params_details.set_title("Simulation Parameters")
        params_details.text(0,1, self.GetParamDetails(grid, steps, convergence), transform=params_details.transAxes, verticalalignment='top')

        self.fig.colorbar(pressure_plot, ax=pressure)
        self.fig.colorbar(vorticity_plot, ax=vorticity)
        self.fig.tight_layout()
        plt.pause(0.001)
        return

    def SavePlot(self):
        plt.savefig(f'cfd.Re_{self.RE:.1f}.png', dpi=150,bbox_inches='tight')
        return

    def GetParamDetails(self, grid, steps, convergence):
        details = ""
        details += f"Simulation step: {steps} \n"
        details += f"h constant (dy or dx): {self.h} \n"
        details += f"nu constant (kinematic velocity): {self.nu} \n"
        details += f"timestep: {self.timestep} \n"
        details += f"rho: {self.rho} \n"
        details += f"convergence factor: {convergence} \n"
        details += f"Reynolds Number (Re): {self.RE:.1f}"
        return details