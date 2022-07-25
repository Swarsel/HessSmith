import numpy as np


def cylinder(radius=1, alpha=360, na=8):
    if int(alpha) == 360:
        a = np.linspace(0, alpha, num=na, endpoint=False) / 180 * np.pi
    else:
        a = np.linspace(0, alpha, num=na) / 180 * np.pi

    x = radius * np.cos(a)
    y = radius * np.sin(a)

    # the following lines are only needed to close the loop for plotting
    #x = np.append(x, np.array(x[0]))
    #y = np.append(y, np.array(y[0]))
    return x, y