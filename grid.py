import numpy as np
class Grid:  
    def __init__ (self, h, firstX, secondX, firstY, secondY):
        x = np.linspace(firstX, secondX, num=int((secondX-firstX)/h)+1)
        y = np.linspace(firstY, secondY, num=int((secondY-firstY)/h)+1)
        self.xv, self.yv = np.meshgrid(x,y)
        self.u = np.zeros(self.xv.shape)
        self.v = np.zeros(self.xv.shape)
        self.p = np.zeros(self.xv.shape)

grid = Grid(0.1, 0, 1, 0, 1)
print(grid.xv)
print(grid.yv)
print(grid.u)
print(grid.v)
print(grid.p)
