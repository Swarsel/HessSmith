from helper import make_continuuous_loop, parsecoords, make_panels
from profile import AirfoilProfile
import numpy
from panel import Panel
from math import atan2


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
    panels: 1D Numpy array of Panel objects.
        The list of panels.
    """

    R = (x.max() - x.min()) / 2.0  # circle radius
    x_center = (x.max() + x.min()) / 2.0  # x-coordinate of circle center

    theta = numpy.linspace(0.0, 2.0 * numpy.pi, N + 1)  # array of angles
    x_circle = x_center + R * numpy.cos(theta)  # x-coordinates of circle

    x_ends = numpy.copy(x_circle)  # x-coordinate of panels end-points
    y_ends = numpy.empty_like(x_ends)  # y-coordinate of panels end-points

    # extend coordinates to consider closed surface
    x, y = numpy.append(x, x[0]), numpy.append(y, y[0])

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
    panels = numpy.empty(N, dtype=object)
    for i in range(N):
        panels[i] = Panel(x_ends[i], y_ends[i], x_ends[i + 1], y_ends[i + 1])

    return panels

filename = "NACA0012.DAT"
make_continuuous_loop(filename)

x, y = parsecoords("data/processeddata/" + filename)
#print((atan2(y[len(x)-2] - y[len(x)-1],x[len(x)-2] - x[len(x)-1])+2*numpy.pi)*180/numpy.pi)

#x = numpy.flipud(x)
#y = numpy.flipud(y)
panels = define_panels(x, y, N=40)
print([(panel.xa, panel.ya, panel.xb, panel.yb) for panel in panels])
profile = AirfoilProfile(panels, filename)

profile.write_panels()
profile.solve()
print(profile)



profile.plot()