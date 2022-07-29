import numpy as np


def cylinder(r=1, n=8):
    # generate a cylinder with n equidistant panels
    a = np.linspace(0, 360, num=n+1, endpoint=True) / 180 * np.pi

    x = r * np.cos(a)
    y = r * np.sin(a)

    return x, y


def circle(radius=1, cx=0, cy=0, N=100):
    theta = np.linspace(0.0, 2 * np.pi, N)
    x_cylinder, y_cylinder = (cx + radius * np.cos(theta),
                              cy + radius * np.sin(theta))
    return x_cylinder, y_cylinder
