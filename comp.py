import numpy as np


def xi(profile):
    panels = profile.panels
    n = len(panels)
    Xi = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            pi, pj = panels[i], panels[j]
            Xi[i][j] = (pi.xm - pj.xm) * np.cos(pj.theta) + (pi.ym - pj.ym) * np.sin(pj.theta)
    return Xi


def eta(profile):
    panels = profile.panels
    n = len(panels)
    Eta = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            pi, pj = panels[i], panels[j]
            Eta[i][j] = -(pi.xm - pj.xm) * np.sin(pj.theta) + (pi.ym - pj.ym) * np.cos(pj.theta)
    return Eta


def I(profile):
    panels = profile.panels
    Xi = profile.xi
    Eta = profile.eta
    n = len(panels)
    II = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            pi, pj = panels[i], panels[j]
            if i == j:
                II[i][j] = 0
            else:
                II[i][j] = 1 / (4 * np.pi) * np.log(((pj.length + 2 * Xi[i][j]) ** 2 + 4 * Eta[i][j] ** 2) /
                                                    ((pj.length - 2 * Xi[i][j]) ** 2 + 4 * Eta[i][j] ** 2))
    return II


def J(profile):
    panels = profile.panels
    Xi = profile.xi
    Eta = profile.eta
    n = len(panels)
    JJ = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            pi, pj = panels[i], panels[j]
            if i == j:
                JJ[i][j] = 0.5
            else:
                JJ[i][j] = (1 / (2 * np.pi)) * np.arctan2(pj.length - 2 * Xi[i][j], 2 * Eta[i][j]) + \
                           (1 / (2 * np.pi)) * np.arctan2(pj.length + 2 * Xi[i][j], 2 * Eta[i][j])
    return JJ


def An(profile):
    panels = profile.panels
    II = profile.I
    JJ = profile.J
    n = len(panels)
    AN = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            pi, pj = panels[i], panels[j]
            AN[i][j] = - np.sin(pi.theta - pj.theta) * II[i][j] + np.cos(pi.theta - pj.theta) * JJ[i][j]
    return AN


def At(profile):
    panels = profile.panels
    II = profile.I
    JJ = profile.J
    n = len(panels)
    AT = np.empty((n, n), dtype=float)
    for i in range(n):
        for j in range(n):
            pi, pj = panels[i], panels[j]
            AT[i][j] = np.cos(pi.theta - pj.theta) * II[i][j] + np.sin(pi.theta - pj.theta) * JJ[i][j]
    return AT


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
        MM[:-1, -1] = np.sum(AT, axis=1)

        r = np.empty(n + 1, dtype=float)
        r[:-1] = AT[0, :] + AT[-1, :]
        r[-1] = -np.sum(AN[0, :] + AN[-1, :])
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
