import numpy as np
from math import atan2

def compute_xi_free(n: int, plen, panels, x, y):
    xi = np.empty((n, plen))

    for i in range(n):
        for j in range(plen):
            xi[i][j] = (x[i] - panels[j].xm) * np.cos(panels[j].theta) + (y[i] - panels[j].ym) * np.sin(
                panels[j].theta)
    return xi


def compute_eta_free(n: int, plen, panels, x, y):
    eta = np.empty((n, plen))

    for i in range(n):
        for j in range(plen):
            eta[i][j] = -(x[i] - panels[j].xm) * np.sin(panels[j].theta) + (
                    y[i] - panels[j].ym) * np.cos(panels[j].theta)
    return eta

def compute_I_free(n: int, plen, xi, eta, panels):
    I = np.empty((n, plen))
    for i in range(n):
        for j in range(plen):
            #print(panels[j].length)
            if i == j:
                I[i][j] = 0
            else:
                I[i][j] = 1 / (4 * np.pi) * np.log(((panels[j].length + 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2) /
                                                   ((panels[j].length - 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2))
    return I


def compute_J_free(n: int, plen, xi, eta, panels):
    J = np.empty((n, plen))
    for i in range(n):
        for j in range(plen):
            if i == j:
                J[i][j] = -0.5
            else:
                J[i][j] = 1 / (2 * np.pi) * atan2(panels[j].length - 2 * xi[i][j], 2 * eta[i][j]) + \
                          1 / (2 * np.pi) * atan2(panels[j].length + 2 * xi[i][j], 2 * eta[i][j])
    return J

def compute_An_free(n: int, plen, I, J, panels):
    A_n = np.empty((n, n))
    for i in range(n):
        for j in range(plen):
            A_n[i][j] = - np.sin(- panels[j].theta) * I[i][j] + np.cos(
                - panels[j].theta) * J[i][j]
    return A_n


def compute_At_free(n: int, plen, I, J, panels):
    A_t = np.empty((n, plen))
    for i in range(n):
        for j in range(plen):
            A_t[i][j] = np.cos(- panels[j].theta) * I[i][j] + np.sin(
                - panels[j].theta) * J[i][j]
    return A_t

def M(profile):
    panels = profile.panels
    AN = profile.An
    AT = profile.At
    vortex = profile.vortex
    n = len(panels)
    if vortex:
        MM = np.empty((n + 1, n + 1), dtype=float)
    else:
        MM = np.empty((n, n), dtype=float)
    if vortex:
        MM[:-1, :-1] = AN
        MM[:-1, -1] = -np.sum(AT, axis=1)

        r = np.empty(n + 1, dtype=float)
        r[:-1] = AT[0, :] + AT[-1, :]
        r[-1] = np.sum(AN[0, :] + AN[-1, :])
        MM[-1, :] = r
    else:
        MM = AN
    return MM


def b(profile, V, a):
    panels = profile.panels
    vortex = profile.vortex
    n = len(panels)
    if vortex:
        B = np.empty(n + 1, dtype=float)
    else:
        B = np.empty(n, dtype=float)
    for i in range(n):
        pi = panels[i]
        B[i] = -V * np.sin(a - pi.theta)
    if vortex:
        B[-1] = -V * (np.cos(a - panels[0].theta) + np.cos(a - panels[-1].theta))
    return B


def q(profile, B):
    panels = profile.panels
    qs = np.linalg.solve(profile.M, B)

    for i, panel in enumerate(panels):
        panel.q = qs[i]
    if profile.vortex:
        profile.gamma = qs[-1]


def vt(profile, V, a):
    panels = profile.panels
    AN = profile.An
    AT = profile.At
    n = len(panels)
    if profile.vortex:
        VT = np.empty(n + 1, dtype=float)
        for i in range(n):
            VT[i] = sum([AT[i][j] * panels[j].q for j in range(n)]) \
                    - profile.gamma * sum([AN[i][j] for j in range(n)]) \
                    + V * np.cos(a - panels[i].theta)
    else:
        VT = np.empty(n, dtype=float)
        for i in range(n):
            VT[i] = sum([AT[i][j] * panels[j].q for j in range(n)]) \
                    + V * np.cos(a - panels[i].theta)
    for i, panel in enumerate(panels):
        panel.vt = VT[i]


def cp(profile, V):
    for panel in profile.panels:
        panel.cp = 1 - (panel.vt / V) ** 2


def ca(profile, V):
    profile.ca = 2 / (V * profile.t) * sum([panel.vt * panel.length for panel in profile.panels])


def accuracy(profile):
    profile.accuracy = sum([panel.q * panel.length for panel in profile.panels])
