from typing import Any


import numpy as np 
import math
import differentials
from grid import Grid
from differentials import Differentials
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
    def AdvectionTerm(self, grid):
        differential = Differentials()
        u_advection = np.zeros_like(grid.u)
        v_advection = np.zeros_like(grid.v)
        for i in range(1, grid.u.shape[0] - 1, 1):
            for j in range(1, grid.u.shape[1] - 1, 1):
                du_dx = 0
                du_dy = 0
                dv_dx = 0
                dv_dy = 0
                if (grid.u[i,j] > 0):
                    du_dx = differential.backwardDifference(grid.u[i-1, j], grid.u[i,j], grid.h)
                    dv_dx = differential.backwardDifference(grid.v[i-1,j], grid.v[i,j], grid.h)

                else:
                    du_dx = differential.forwardDifference(grid.u[i+1,j], grid.u[i, j], grid.h)
                    dv_dx = differential.forwardDifference(grid.v[i+1, j], grid.v[i,j], grid.h)


                if (grid.v[i,j] > 0):
                    du_dy = differential.backwardDifference(grid.u[i, j - 1], grid.u[i,j], grid.h)
                    dv_dy = differential.backwardDifference(grid.v[i, j -1], grid.v[i,j], grid.h)
                    
                else:
                    du_dy = differential.forwardDifference(grid.u[i,j+1], grid.u[i,j], grid.h)
                    dv_dy = differential.forwardDifference(grid.v[i, j+1], grid.v[i,j], grid.h)


                u_advection[i,j] = grid.u[i,j] * du_dx + grid.v[i,j] * du_dy
                v_advection[i,j] = grid.u[i,j] * dv_dx + grid.v[i,j] * dv_dy

        return u_advection, v_advection
    
    def ViscosityTerm(self, grid, nu):
        differentials = Differentials()
        u_viscosity = np.zeros_like(grid.u)
        v_viscosity = np.zeros_like(grid.v)
        for i in range(1, grid.u.shape[0] - 1, 1):
            for j in range(1, grid.v.shape[1] - 1, 1):
                u_viscosity[i,j] = nu * (differentials.centralDifference(grid.u[i+1, j], grid.u[i,j], grid.u[i-1,j], grid.h) + differentials.centralDifference(grid.u[i, j+1], grid.u[i, j], grid.u[i, j-1], grid.h))
                v_viscosity[i,j] = nu * (differentials.centralDifference(grid.v[i+1,j], grid.v[i,j], grid.v[i-1,j], grid.h) + differentials.centralDifference(grid.v[i,j+1], grid.v[i,j], grid.v[i,j-1], grid.h))
        return u_viscosity, v_viscosity
    
    def VelocityStep(self, u, v, u_viscosity, v_viscosity, u_advection, v_advection, delta_t):
        u_star = np.zeros_like(u)
        v_star = np.zeros_like(v)
        u_star = u + delta_t * (-u_advection + u_viscosity)
        v_star = v + delta_t * (-v_advection + v_viscosity)
        return u_star, v_star
grid = Grid(0.1, 0, 1, 0, 1)
Solver().PoissonSolver(grid.p, np.zeros(grid.p.shape), grid.h, 0.1, 100)