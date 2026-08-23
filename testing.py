import math
from grid import Grid
from solver import Solver
def forward(x, h):
    return (math.sin(x+h) - math.sin(x)) / h

def backward(x, h):
    return (math.sin(x) - math.sin(x-h)) / h

def centralFirst(x, h):
    return (math.sin(x+h) - math.sin(x - h)) / (2*h)

def centralSecond(x, h):
    return (math.sin(x+h) - 2*math.sin(x) + math.sin(x - h)) / math.pow(h, 2)

def FirstPrinciplesTesting():
    print("Cos(5) = " + str(math.cos(5)))
    print(forward(5, 1))
    print(backward(5, 1))
    print(centralFirst(5, 1))
    print(centralSecond(5, 1))

    print(forward(5, 0.1))
    print(backward(5, 0.1))
    print(centralFirst(5, 0.1))
    print(centralSecond(5, 0.1))

grid = Grid(0.1, 0, 1, 0, 1)
print(len(grid.p))
print(grid.p.shape[0])