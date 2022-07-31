from make_cylinder import cylinder, circle
from helper import make_panels, write_coords, parsecoords, make_panels_ant
from profile import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot
from panel import Panel


def define_panels(x, y, N=40):
    """
    Discretizes the geometry into panels using 'cosine' method.

    Parameters
    ----------
    x: 1D array of floats
        x-coordinate of the points defining the geometry.
    y: 1D array of floats
        y-coordinate of the points defining the geometry.
    N: integer, optional
        Number of panels;
        default: 40.

    Returns
    -------
    panels: 1D np array of Panel objects.
        The list of panels.
    """

    R = (x.max() - x.min()) / 2.0  # circle radius
    x_center = (x.max() + x.min()) / 2.0  # x-coordinate of circle center

    theta = np.linspace(0.0, 2.0 * np.pi, N + 1)  # array of angles
    x_circle = x_center + R * np.cos(theta)  # x-coordinates of circle

    x_ends = np.copy(x_circle)  # x-coordinate of panels end-points
    y_ends = np.empty_like(x_ends)  # y-coordinate of panels end-points

    # extend coordinates to consider closed surface
    x, y = np.append(x, x[0]), np.append(y, y[0])

    # compute y-coordinate of end-points by projection
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

    # create panels
    panels = np.empty(N, dtype=object)
    for i in range(N):
        panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i + 1], y_ends[i + 1])
    return panels

cas = []
aas = []
x, y = parsecoords("data/processeddata/naca0012b.dat")
x = np.append(x, x[0])
y = np.append(y, y[0])
x = np.flipud(x)
y = np.flipud(y)

panels = make_panels_ant(x, y)
print([(p.xa, p.ya) for p in panels])
print(panels[-1].xb, panels[-1].yb)
profile = AirfoilProfile(panels, f"NACA0012", vortex=True)

#for a in range(-25,25):
    #print(npanels)
a=4.0
profile.solve(a=np.radians(a))
print(profile)
cas.append(profile.ca)
aas.append(a)

    #pyplot.plot(n, y, color='g', linestyle=':', linewidth=1)

"""
pyplot.figure(figsize=(5, 5))
pyplot.grid()
pyplot.xlabel("$\\alpha$", fontsize=16)
pyplot.ylabel('$c_a$', fontsize=16)
print(aas, cas)
pyplot.plot(aas, cas, 'k:', markersize=1)
pyplot.show()
"""