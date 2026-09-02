from boundary import BoundaryConditions
from grid import Grid
from solver import Solver
from differentials import Differentials
from visualisation import Visualisation
from tests import Tests
import numpy as np

test_cases = Tests()
case = test_cases.SelectTestCase()

H = case["h"]
NU = case["nu"]
TIMESTEP = case["timestep"]
RHO = case["rho"]
TOLERANCE = case["tolerance"]
MAX_ITERATIONS = case["max_iterations"]
CONVERGENCE_TOLERANCE = case["convergence_tolerance"]
LID_VELOCITY = case["lid_velocity"]
CAVITY_WIDTH = 1

boundary_conditions = BoundaryConditions(LID_VELOCITY)
solver = Solver()
grid = Grid(H, 0, 1, 0,1)
visualise = Visualisation(grid, H, NU, TIMESTEP, RHO,LID_VELOCITY, CAVITY_WIDTH, case["ghia_y"], case["ghia_u"])

grid.u, grid.v = boundary_conditions.ApplyBoundaryConditions(grid.u, grid.v)
grid.p = boundary_conditions.ApplyPressureBoundary(grid.p)

play = True
steps = 0
u_before = np.zeros_like(grid.u)
v_before = np.zeros_like(grid.v)

visualise.Visualise(grid, steps, np.max(np.abs(grid.u - u_before)))
try:
    while play:
        steps += 1
        
        u_before = np.copy(grid.u)
        v_before = np.copy(grid.v)

        u_advection, v_advection = solver.AdvectionTerm(grid)
        u_viscosity, v_viscosity = solver.ViscosityTerm(grid, NU)

        u_star, v_star = solver.VelocityStep(grid.u, grid.v, u_viscosity, v_viscosity, u_advection, v_advection, TIMESTEP)
        u_star, v_star = boundary_conditions.ApplyBoundaryConditions(u_star, v_star)

        f = solver.Divergence(u_star, v_star, H, RHO, TIMESTEP)

        p = solver.PoissonSolver(grid.p, f, H, TOLERANCE, MAX_ITERATIONS)
        # p = solver.SmoothPressure(p)  # DISABLED: smoother amplifies errors instead of damping them
        p = boundary_conditions.ApplyPressureBoundary(p)

        u_calculated, v_calculated = solver.PressureCorrection(u_star, v_star, p, RHO, TIMESTEP, H)
        u_calculated, v_calculated = boundary_conditions.ApplyBoundaryConditions(u_calculated, v_calculated)

        grid.u = np.copy(u_calculated)
        grid.v = np.copy(v_calculated)
        grid.p = np.copy(p)

        grid.vorticity = solver.Vorticity(grid.u, grid.v, H)

        if steps % 40 == 0:
            visualise.Visualise(grid, steps, np.max(np.abs(grid.u - u_before)))

        if np.max(np.abs(grid.u - u_before)) <= CONVERGENCE_TOLERANCE and np.max(np.abs(grid.v - v_before)) <= CONVERGENCE_TOLERANCE:
            break

    visualise.Visualise(grid, steps, np.max(np.abs(grid.u - u_before)))
    visualise.SavePlot()

except KeyboardInterrupt:
    visualise.Visualise(grid, steps,np.max(np.abs(grid.u - u_before)))
    visualise.SavePlot()
    print("Application quit")
