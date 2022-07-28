import numpy as np


def cylinder(radius=1, n=8):
    # generate a cylinder with n equidistant panels
    a = np.linspace(0, 360, num=n+1, endpoint=True) / 180 * np.pi

    x = radius * np.cos(a)
    y = radius * np.sin(a)

    return x, y
