import numpy as np

def GenGrid(h, firstX, secondX, firstY, secondY):
    x = np.linspace(firstX, secondX, num=int(1/(secondX-firstX)/h)+1)
    y = np.linspace(firstY, secondY, num=int(1/(secondY-firstY)/h)+1)
    xv, yv = np.meshgrid(x,y)
    u = np.zeros(xv.shape)
    v = np.zeros(xv.shape)
    p = np.zeros(xv.shape)
    return xv, yv, u, v, p

xv, yv, u, v, p = GenGrid(0.1, 0, 1, 0, 1)
print(xv)
print(yv)
print(u)
print(v)
print(p)
