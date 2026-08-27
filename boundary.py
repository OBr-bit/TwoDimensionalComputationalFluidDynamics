class BoundaryConditions:
    def ApplyBoundaryConditions(self, u, v):
        u[0, :] = 0
        u[-1, :] = 1.0
        u[:, 0] = 0
        u[:, -1] = 0
        v[0, :] = 0
        v[-1, :] = 0
        v[:, 0] = 0
        v[:, -1] = 0
        return u, v