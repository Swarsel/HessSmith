import numpy as np

def cylinder(radius=1, n=8):
    # generate a cylinder with n equidistant panels
    a = np.linspace(0, 360, num=n, endpoint=False) / 180 * np.pi

    x = radius * np.cos(a)
    y = radius * np.sin(a)

    # the following lines are only needed to close the loop for plotting
    #x = np.append(x, np.array(x[0]))
    #y = np.append(y, np.array(y[0]))
    return x, y