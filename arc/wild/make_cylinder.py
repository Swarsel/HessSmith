import numpy as np


def cylinder(r=0.5, cx= 0.5, cy= 0, n=8):
    # generate a cylinder with n equidistant panels
    a = np.linspace(0, 360, num=n+1, endpoint=True) / 180 * np.pi

    x = cx + r * np.cos(a)
    y = cy + r * np.sin(a)
    if abs(x[0] - x[-1]) <= 10 ** (-15):
        x[-1] = x[0]
    if abs(y[0] - y[-1]) <= 10 ** (-15):
        y[-1] = y[0]

    return x, y, r


def circle(radius=0.5, cx=0.5, cy=0, N=100):
    theta = np.linspace(0.0, 2 * np.pi, N)
    x_cylinder, y_cylinder = (cx + radius * np.cos(theta),
                              cy + radius * np.sin(theta))
    return x_cylinder, y_cylinder, radius
