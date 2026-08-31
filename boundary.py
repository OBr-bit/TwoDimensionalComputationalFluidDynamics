class BoundaryConditions:
    def __init__(self, velocity) -> None:
        self.inlet_velocity = velocity
    def ApplyBoundaryConditions(self, u, v):
        u[0, :] = 0
        u[-1, :] = self.inlet_velocity
        u[:, 0] = 0
        u[:, -1] = 0
        v[0, :] = 0
        v[-1, :] = 0
        v[:, 0] = 0
        v[:, -1] = 0
        return u, v
         
    def ApplyPressureBoundary(self, p):
        p[0, :] = p[1, :]    # bottom
        p[-1, :] = p[-2, :]  # top
        p[:, 0] = p[:, 1]    # left
        p[:, -1] = p[:, -2]  # right
        return p