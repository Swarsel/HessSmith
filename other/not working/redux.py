from math import atan2
import numpy as np
from panel import Panel


def make_panels(x, y):
    panels = np.empty(len(x)-1, dtype=object)
    for i in range(len(x)-1):
        panels[i] = Panel(x[-i-2], y[-i-2], x[-i-1], y[-i-1])
    if (panels[0].xa, panels[0].ya) == (panels[0].xb, panels[0].yb):
        panels = panels[1:]
    return panels


def parsecoords(filename: str):
    xis, yis = np.loadtxt(filename, dtype=float, unpack=True)
    return xis, yis

def compute_xi(n: int, panels):
    xi = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            xi[i][j] = (panels[i].xm - panels[j].xm) * np.cos(panels[j].theta) + (panels[i].ym - panels[j].ym) * np.sin(
                panels[j].theta)
    return xi


def compute_eta(n: int, panels):
    eta = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            eta[i][j] = -(panels[i].xm - panels[j].xm) * np.sin(panels[j].theta) + (
                    panels[i].ym - panels[j].ym) * np.cos(panels[j].theta)
    return eta


def compute_I(n: int, xi, eta, panels):
    I = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                I[i][j] = 0
            else:
                I[i][j] = 1 / (4 * np.pi) * np.log(((panels[j].length + 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2) /
                                                   ((panels[j].length - 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2))
    return I


def compute_J(n: int, xi, eta, panels):
    J = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                J[i][j] = 0.5
            else:
                J[i][j] = 1 / (2 * np.pi) * atan2(panels[j].length - 2 * xi[i][j], 2 * eta[i][j]) + \
                          1 / (2 * np.pi) * atan2(panels[j].length + 2 * xi[i][j], 2 * eta[i][j])
    return J

def compute_An(n: int, I, J, panels):
    #print(I[0][n-1], J[0][n-1], panels[0].theta, panels[-1].theta)
    A_n = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            #if i == j:
                A_n[i][j] = - np.sin(panels[i].theta - panels[j].theta) * I[i][j] + np.cos(
                panels[i].theta - panels[j].theta) * J[i][j]
            #else:
             #  A_n[i][j] = np.sin(panels[i].theta - panels[j].theta) * I[i][j] - np.cos(
              #    panels[i].theta - panels[j].theta) * J[i][j]
    return A_n



def compute_At(n: int, I, J, panels):
    A_t = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            A_t[i][j] = np.cos(panels[i].theta - panels[j].theta) * I[i][j] + np.sin(
                panels[i].theta - panels[j].theta) * J[i][j]
    return A_t


def kutta_condition(A_n, A_t):
    v = np.empty(A_n.shape[0] + 1, dtype=float)
    v[:-1] = A_t[0, :] + A_t[-1, :]
    v[-1] = - np.sum(A_n[0, :] + A_n[-1, :])
    return v


def system_matrix(A_n, A_t, vortex=True):
    if vortex:
        M = np.empty((A_n.shape[0] + 1, A_n.shape[1] + 1), dtype=float)
    else:
        M = np.empty((A_n.shape[0], A_n.shape[1]), dtype=float)
    if vortex:
        M[:-1, :-1] = A_n
        M[:-1, -1] = np.sum(A_t, axis=1)
        M[-1, :] = kutta_condition(A_n, A_t)
    else:
        M = A_n
    return M


def compute_inhomogenity(panels, vortex, V, a):
    if vortex:
        b = np.empty(panels.size + 1, dtype=float)
    else:
        b = np.empty(panels.size, dtype=float)
    for i, panel in enumerate(panels):
        b[i] = -V * np.sin(a - panel.theta)
    # b_n
    if vortex:
        b[-1] = -V * (np.cos(a - panels[0].theta) + np.cos(a - panels[-1].theta))
    return b


class Panel:

    def __init__(self, xa, ya, xb, yb):
        self.xa, self.ya = xa, ya  # panel starting-point
        self.xb, self.yb = xb, yb  # panel ending-point

        self.xm = (xa + xb) / 2  # center of panel on x axis
        self.ym = (ya + yb) / 2  # center of panel on y axis
        self.length = np.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)  # panel length
        self.theta = atan2(yb - ya, xb - xa)  # angle of panel
        if self.theta < 0:
            self.theta += 2*np.pi

        self.q = None  # source strength
        self.vt = None  # tangential velocity
        self.cp = None  # pressure coefficient

    def set_theta(self, theta):
        self.theta = theta


class AirfoilProfile:
    def __init__(self, panels, name, vortex=True):
        self.panels = panels
        self.name = name
        self.len = len(self.panels)
        self.vortex = vortex
        self.ca = None
        self.accuracy = None
        self.gamma = None

        self.U = sum([panel.length for panel in self.panels])
        self.xi = compute_xi(self.len, self.panels)
        self.eta = compute_eta(self.len, self.panels)
        self.I = compute_I(self.len, self.xi, self.eta, self.panels)
        self.J = compute_J(self.len, self.xi, self.eta, self.panels)
        self.An = compute_An(self.len, self.I, self.J, self.panels)
        self.At = compute_At(self.len, self.I, self.J, self.panels)
        self.M = system_matrix(self.An, self.At, self.vortex)

        self.coords = [(panel.xa, panel.ya, panel.xb, panel.yb) for panel in self.panels]
        self.x = [panel.xa for panel in self.panels]
        self.y = [panel.ya for panel in self.panels]
        self.t = abs(max(self.x) - min(self.x))



    def __str__(self):
        return f"Theta:\n" \
               f"{[panel.theta * 180 / np.pi for panel in self.panels]}\n" \
               f"I:\n" \
               f"{self.I}\n" \
               f"J:\n" \
               f"{self.J}\n" \
               f"M:\n" \
               f"{self.M}\n" \
               f"An:\n" \
               f"{self.An}\n" \
               f"At:\n" \
               f"{self.At}\n" \
               f"Source:\n" \
               f"{[panel.q for panel in self.panels]}\n" \
               f"vt:\n" \
               f"{[panel.vt for panel in self.panels]}\n" \
               f"Pressure coefficients:\n" \
               f"{[panel.cp for panel in self.panels]}\n" \
               f"Accuracy:\n" \
               f"{self.accuracy}\n" \
               f"gamma:\n" \
               f"{self.gamma}\n" \
               f"Lift coefficient:\n" \
               f"{self.ca}"

    def solve(self, V=1, a=np.radians(4.0)):
        b = compute_inhomogenity(self.panels, self.vortex, V, a)
        qs = np.linalg.solve(self.M, b)
        #print(b)
        for i, panel in enumerate(self.panels):
            panel.q = qs[i]
        if self.vortex:
            self.gamma = qs[-1]

        if self.vortex:
            vt = []
            for i in range(self.len):
                vt.append(
                    sum([self.At[i][j] * self.panels[j].q for j in range(self.len)]) - self.gamma * sum(
                        [self.An[i][j] for j in range(self.len)]) + V * np.cos(
                        a - self.panels[i].theta))
        else:
            vt = []
            for i in range(self.len):
                vt.append(
                    sum([self.At[i][j] * self.panels[j].q for j in range(self.len)]) + V * np.cos(
                        a - self.panels[i].theta))
        for i, panel in enumerate(self.panels):
            panel.vt = vt[i]

        for panel in self.panels:
            panel.cp = 1 - (panel.vt / V) ** 2

        self.ca = 2 / (V * self.t) * sum([panel.vt * panel.length for panel in self.panels])
        self.accuracy = sum([panel.q * panel.length for panel in self.panels])


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
    y_ends = np.flipud(y_ends)
    x_ends = np.flipud(x_ends)

    # create panels
    panels = np.empty(N, dtype=object)
    for i in range(N):
        #print(f"Connecting {x_ends[i], y_ends[i]} to {x_ends[i + 1], y_ends[i + 1]}")
        panels[i] = Panel(x_ends[i], y_ends[i],x_ends[i + 1], y_ends[i + 1])
        #print(f"Angle is {panels[i].theta*180/np.pi}")

    return panels



cas = []
aas = []
#x, y = parsecoords("data/processeddata/naca0012b.dat")
with open("data/processeddata/naca0012b.dat", 'r') as infile:
    x, y = np.loadtxt(infile, dtype=float, unpack=True)
x, y = np.append(x, x[0]), np.append(y, y[0])
#x = np.flipud(x)
#y = np.flipud(y)
panels = make_panels(x, y)
#print([(panel.xa,panel.ya) for panel in panels])
profile = AirfoilProfile(panels, f"NACA0012", vortex=True)
#print([(a,b) for a,b in zip(x,y)])
n = len(panels)
teta = []
for i in range(len(panels)):
    tt = atan2(y[n-i-i] - y[n-i], x[n-i-1] - x[n-1])
    teta.append(tt)
#print(teta)

for i in range(n):
    panels[i].set_theta(teta[i])

profile.solve()
print(profile)
# for a in range(-25,25):
# print(npanels)
#print(panels[-1].xa, panels[-1].ya, panels[-1].xb, panels[-1].yb, panels[-1].theta)
#print(atan2(1-0.9938441702975689, 0-0.0021202043318089836))
#with np.printoptions(threshold=np.inf):
#    print(profile.An)
"""

c1 = [(panel.xa,panel.ya) for panel in panels]


check = [(1.0, 0.0), (0.9938441702975689, 0.0021202043318089836), (0.9755282581475768, 0.004641295059216982), (0.9455032620941839, 0.008656068833462427), (0.9045084971874737, 0.013914300349052097), (0.8535533905932737, 0.02010348671099793), (0.7938926261462366, 0.02689882023587635), (0.7269952498697734, 0.033956565674892164), (0.6545084971874737, 0.04091740025026903), (0.5782172325201155, 0.04737352132236092), (0.5, 0.052924299999999994), (0.4217827674798846, 0.05713321271252607), (0.34549150281252633, 0.05957469993528279), (0.2730047501302266, 0.059825735412326046), (0.2061073738537635, 0.05767983320529529), (0.14644660940672627, 0.05305394437923077), (0.09549150281252633, 0.04604890046158151), (0.054496737905816106, 0.03682192386786797), (0.024471741852423234, 0.025809478510129633), (0.00615582970243117, 0.013388097223224732), (0.0, 0.0), (0.006155829702431115, -0.013388097223224676), (0.02447174185242318, -0.02580947851012961), (0.05449673790581605, -0.03682192386786795), (0.09549150281252627, -0.0460489004615815), (0.14644660940672616, -0.05305394437923076), (0.20610737385376338, -0.05767983320529528), (0.2730047501302265, -0.05982573541232604), (0.3454915028125262, -0.0595746999352828), (0.42178276747988447, -0.05713321271252608), (0.4999999999999999, -0.0529243), (0.5782172325201154, -0.047373521322360924), (0.6545084971874736, -0.040917400250269034), (0.7269952498697734, -0.033956565674892164), (0.7938926261462365, -0.026898820235876364), (0.8535533905932737, -0.020103486710997917), (0.9045084971874737, -0.013914300349052097), (0.9455032620941839, -0.008656068833462427), (0.9755282581475768, -0.00464129505921701), (0.9938441702975689, -0.0021202043318089836)]

for i in range(len(c1)):
    if round(c1[i][0],7) == round(check[i][0],7):
        print("ya")
    else:
        print("no")

#print(profile.coords)
profile.solve()
print(profile)
#cas.append(profile.ca)
#aas.append(a)

# pyplot.plot(n, y, color='g', linestyle=':', linewidth=1)
"""
"""
pyplot.figure(figsize=(5, 5))
pyplot.grid()
pyplot.xlabel("$\\alpha$", fontsize=16)
pyplot.ylabel('$c_a$', fontsize=16)
print(aas, cas)
pyplot.plot(aas, cas, 'k:', markersize=1)
pyplot.show()
"""