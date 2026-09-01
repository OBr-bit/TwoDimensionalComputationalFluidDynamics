import numpy as np 
import math
from grid import Grid
from differentials import Differentials

class Solver:
    def __init__(self) -> None:
        self.differential = Differentials()

    def PoissonSolver(self, p, f, h, tolerance, maxRuns):
        before = np.zeros_like(p)
        runs = 0
        while True:
            before = np.copy(p)
            for i in range(1, p.shape[0] - 1, 1):
                for j in range(1, p.shape[1] - 1, 1):
                    p[i,j] = (p[i+1, j] + p[i-1,j] + p[i, j+1] + p[i,j-1] - math.pow(h, 2) * f[i,j]) / 4

            runs = runs + 1
            if (np.max(np.abs(p - before)) <= tolerance or runs > maxRuns):
                break
            
        return p

    def SmoothPressure(self, p):
        smooth = np.zeros_like(p)
        for i in range(1, p.shape[0] - 1, 1):
            for j in range(1, p.shape[1] - 1, 1):
                smooth[i,j] = (p[i,j] + p[i-1,j] + p[i+1,j] + p[i,j-1] + p[i,j+1]) / 5
        return smooth

    def AdvectionTerm(self, grid):
        u_advection = np.zeros_like(grid.u)
        v_advection = np.zeros_like(grid.v)
        for i in range(1, grid.u.shape[0] - 1, 1):
            for j in range(1, grid.u.shape[1] - 1, 1):
                du_dx = 0
                du_dy = 0
                dv_dx = 0
                dv_dy = 0
                if (grid.u[i,j] > 0):
                    du_dx = self.differential.backwardDifference(grid.u[i, j-1], grid.u[i,j], grid.h)
                    dv_dx = self.differential.backwardDifference(grid.v[i,j-1], grid.v[i,j], grid.h)

                else:
                    du_dx = self.differential.forwardDifference(grid.u[i,j+1], grid.u[i, j], grid.h)
                    dv_dx = self.differential.forwardDifference(grid.v[i, j+1], grid.v[i,j], grid.h)


                if (grid.v[i,j] > 0):
                    du_dy = self.differential.backwardDifference(grid.u[i-1, j], grid.u[i,j], grid.h)
                    dv_dy = self.differential.backwardDifference(grid.v[i-1, j], grid.v[i,j], grid.h)
                    
                else:
                    du_dy = self.differential.forwardDifference(grid.u[i+1,j], grid.u[i,j], grid.h)
                    dv_dy = self.differential.forwardDifference(grid.v[i+1, j], grid.v[i,j], grid.h)

                u_advection[i,j] = grid.u[i,j] * du_dx + grid.v[i,j] * du_dy
                v_advection[i,j] = grid.u[i,j] * dv_dx + grid.v[i,j] * dv_dy
        return u_advection, v_advection
    
    def ViscosityTerm(self, grid, nu):
        u_viscosity = np.zeros_like(grid.u)
        v_viscosity = np.zeros_like(grid.v)
        for i in range(1, grid.u.shape[0] - 1, 1):
            for j in range(1, grid.v.shape[1] - 1, 1):
                u_viscosity[i,j] = nu * (self.differential.centralDifference(grid.u[i,j+1], grid.u[i,j], grid.u[i,j-1], grid.h) + self.differential.centralDifference(grid.u[i+1,j], grid.u[i,j], grid.u[i-1,j], grid.h))
                v_viscosity[i,j] = nu * (self.differential.centralDifference(grid.v[i,j+1], grid.v[i,j], grid.v[i,j-1], grid.h) + self.differential.centralDifference(grid.v[i+1,j], grid.v[i,j], grid.v[i-1,j], grid.h))
        return u_viscosity, v_viscosity
    
    def VelocityStep(self, u, v, u_viscosity, v_viscosity, u_advection, v_advection, delta_t):
        u_star = np.zeros_like(u)
        v_star = np.zeros_like(v)
        u_star = u + delta_t * (-u_advection + u_viscosity)
        v_star = v + delta_t * (-v_advection + v_viscosity)
        return u_star, v_star

    def PressureCorrection(self, u_star, v_star, p, rho, delta_t, h):
        u_calculated = np.zeros_like(u_star)
        v_calculated = np.zeros_like(v_star)
        for i in range(1, u_star.shape[0] - 1, 1):
            for j in range(1, u_star.shape[1] - 1, 1):
                u_calculated[i,j] = u_star[i,j] - (delta_t / rho) * self.differential.centralDifferenceFirst(p[i,j+1], p[i,j-1], h)
                v_calculated[i,j] = v_star[i,j] - (delta_t / rho) * self.differential.centralDifferenceFirst(p[i+1,j], p[i-1,j], h)
        return u_calculated, v_calculated
    
    def Divergence(self, u_star, v_star, h, rho, delta_t):
        f = np.zeros_like(u_star)
        for i in range(1, u_star.shape[0] - 1, 1):
            for j in range(1, u_star.shape[1] - 1, 1):
                f[i,j] = (rho/delta_t) * (self.differential.centralDifferenceFirst(u_star[i, j+1], u_star[i, j-1], h) + self.differential.centralDifferenceFirst(v_star[i+1, j], v_star[i-1, j], h))
        return f

    def Vorticity(self, u, v, h):
        vorticity = np.zeros_like(u)
        for i in range(1, u.shape[0] - 1, 1):
            for j in range(1, u.shape[1] - 1, 1):
                vorticity[i,j] = self.differential.centralDifferenceFirst(v[i, j+1], v[i, j-1], h) - self.differential.centralDifferenceFirst(u[i+1, j], u[i-1, j], h)
        return vorticity