from panel_new import Panel
import numpy as np


def make_panels(x, y, reverse=False):
    if type(x) is not np.ndarray:
        x = np.array(x)
    if type(y) is not np.ndarray:
        y = np.array(y)
    if (x[0], y[0]) != (x[-1], y[-1]):
        x = np.append(x, x[0])
        y = np.append(y, y[0])
    if reverse:
        x = np.flipud(x)
        y = np.flipud(y)
    n = len(x) - 1
    panels = np.array([Panel(x[i], y[i], x[i + 1], y[i + 1]) for i in range(n)])
    return panels


def parsecoords(filename):
    x, y = np.loadtxt(filename, dtype=float, unpack=True)
    return x, y


## only for testing of discretization
def define_panels(x, y, N=40, reverse=False):
    R = (x.max() - x.min()) / 2.0
    x_center = (x.max() + x.min()) / 2.0
    theta = np.linspace(0.0, 2.0 * np.pi, N + 1)
    x_circle = x_center + R * np.cos(theta)
    x_ends = np.copy(x_circle)
    y_ends = np.empty_like(x_ends)
    x, y = np.append(x, x[0]), np.append(y, y[0])
    I = 0
    for i in range(N):
        while I < len(x) - 1:
            if (x[I] <= x_ends[i] <= x[I + 1]) or (x[I + 1] <= x_ends[i] <= x[I]):
                break
            else:
                I += 1
        a = (y[I + 1] - y[I]) / (x[I + 1] - x[I])
        b = y[I + 1] - a * x[I + 1]
        y_ends[i] = a * x_ends[i] + b
    y_ends[N] = y_ends[0]
    if reverse:
        x_ends = np.flipud(x)
        y_ends = np.flipud(y)
    panels = np.empty(N, dtype=object)
    for i in range(N):
        panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i + 1], y_ends[i + 1])

    return panels