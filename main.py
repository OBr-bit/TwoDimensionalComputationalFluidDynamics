from boundary import BoundaryConditions
import boundary
from grid import Grid
from solver import Solver
from differentials import Differentials
from visualisation import Visualisation
import numpy as np

H = 0.05
NU = 0.1
TIMESTEP = 0.005
RHO = 1
TOLERANCE = 0.001
MAX_ITERATIONS = 100
CONVERGENCE_TOLERANCE = 0.00001
boundary_conditions = BoundaryConditions()
solver = Solver()
grid = Grid(H, 0, 1, 0,1)
visualise = Visualisation(grid)

grid.u, grid.v = boundary_conditions.ApplyBoundaryConditions(grid.u, grid.v)
grid.p = boundary_conditions.ApplyPressureBoundary(grid.p)

play = True
steps = 0
u_before = np.zeros_like(grid.u)
v_before = np.zeros_like(grid.v)
try:
    while play:
        u_before = np.copy(grid.u)
        v_before = np.copy(grid.v)
        steps += 1
        u_advection, v_advection = solver.AdvectionTerm(grid)
        u_viscosity, v_viscosity = solver.ViscosityTerm(grid, NU)
        u_star, v_star = solver.VelocityStep(grid.u, grid.v, u_viscosity, v_viscosity, u_advection, v_advection, TIMESTEP)
        u_star, v_star = boundary_conditions.ApplyBoundaryConditions(u_star, v_star)
        f = solver.Divergence(u_star, v_star, H, RHO, TIMESTEP)

        p = solver.PoissonSolver(grid.p, f, H, TOLERANCE, MAX_ITERATIONS)
        p = solver.SmoothPressure(p)
        p = boundary_conditions.ApplyPressureBoundary(p)

        u_calculated, v_calculated = solver.PressureCorrection(u_star, v_star, p, RHO, TIMESTEP, H)

        u_calculated, v_calculated = boundary_conditions.ApplyBoundaryConditions(u_calculated, v_calculated)
        grid.u = np.copy(u_calculated)
        grid.v = np.copy(v_calculated)
        grid.p = np.copy(p)
        grid.vorticity = solver.Vorticity(grid.u, grid.v, H)

        print(steps)
        if steps % 40 == 0:
            visualise.Visualise(grid, steps)
            convergence = np.max(np.abs(grid.u - u_before))
            print(f"Convergence = {convergence}")
        if np.max(np.abs(grid.u - u_before)) <= CONVERGENCE_TOLERANCE and np.max(np.abs(grid.v - v_before)) <= CONVERGENCE_TOLERANCE:
            break
    visualise.Visualise(grid, steps)
    visualise.SavePlot()
except KeyboardInterrupt:
    visualise.Visualise(grid, steps)
    visualise.SavePlot()
    print("Application quit")
