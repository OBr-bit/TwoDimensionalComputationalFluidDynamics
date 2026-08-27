from boundary import BoundaryConditions
import boundary
from grid import Grid
from solver import Solver
from differentials import Differentials
from visualisation import Visualisation
import numpy as np

H = 0.05
TIMESTEP = 0.0005
NU = 0.01
RHO = 1
TOLERANCE = 0.0001
MAX_ITERATIONS = 500
boundary_conditions = BoundaryConditions()
solver = Solver()
visualise = Visualisation()
grid = Grid(H, 0, 1, 0,1)


grid.u, grid.v = boundary_conditions.ApplyBoundaryConditions(grid.u, grid.v)
grid.p = boundary_conditions.ApplyPressureBoundary(grid.p)

play = True
try:
    while play:
        u_advection, v_advection = solver.AdvectionTerm(grid)
        u_viscosity, v_viscosity = solver.ViscosityTerm(grid, NU)

        u_star, v_star = solver.VelocityStep(grid.u, grid.v, u_viscosity, v_viscosity, u_advection, v_advection, TIMESTEP)
        
        f = solver.Divergence(u_star, v_star, H, RHO, TIMESTEP)

        p = solver.PoissonSolver(grid.p, f, H, TOLERANCE, MAX_ITERATIONS)
        p = solver.SmoothPressure(p)
        p = boundary_conditions.ApplyPressureBoundary(p)

        u_calculated, v_calculated = solver.PressureCorrection(u_star, v_star, p, RHO, TIMESTEP, H)

        u_calculated, v_calculated = boundary_conditions.ApplyBoundaryConditions(u_calculated, v_calculated)
        grid.u = np.copy(u_calculated)
        grid.v = np.copy(v_calculated)
        grid.p = np.copy(p)
        #print(grid.u)
        #print(grid.v)
        #print(grid.p)

        visualise.Visualise(grid)

        #response = input()
        #if response != "":
        #    play = False
except KeyboardInterrupt:
    print("Application quit")
