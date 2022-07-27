import numpy as np
from math import atan2


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
    A_n = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            #if i == j:
                A_n[i][j] = - np.sin(panels[i].theta - panels[j].theta) * I[i][j] + np.cos(
                    panels[i].theta - panels[j].theta) * J[i][j]
            #else:
             #   A_n[i][j] =  np.sin(panels[i].theta - panels[j].theta) * I[i][j] - np.cos(
              #      panels[i].theta - panels[j].theta) * J[i][j]
    return A_n


def compute_At(n: int, I, J, panels):
    A_t = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            A_t[i][j] = np.cos(panels[i].theta - panels[j].theta) * I[i][j] + np.sin(
                panels[i].theta - panels[j].theta) * J[i][j]
    return A_t


def compute_M(n: int, A_n):
    M = np.empty((n, n))
    for i in range(n):
        for j in range(n):
                M[i][j] = A_n[i][j]
    return M


def kutta_condition(A_n, A_t):
    b = np.empty(A_n.shape[0] + 1, dtype=float)
    # matrix of source contribution on tangential velocity
    # is the same than
    # matrix of vortex contribution on normal velocity
    b[:-1] = A_t[0, :] + A_t[-1, :]
    # matrix of vortex contribution on tangential velocity
    # is the opposite of
    # matrix of source contribution on normal velocity
    b[-1] = - np.sum(A_n[0, :] + A_n[-1, :])
    return b


def system_matrix(A_n, A_t):
    M = np.empty((A_n.shape[0] + 1, A_n.shape[1] + 1), dtype=float)
    # source contribution matrix
    M[:-1, :-1] = A_n
    # vortex contribution array
    M[:-1, -1] = np.sum(A_t, axis=1)
    # Kutta condition array
    M[-1, :] = kutta_condition(A_n, A_t)
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

def compute_inhomogenity_old(panels, vortex, V, a):
    b = np.empty(panels.size + 1, dtype=float)
    # freestream contribution on each panel
    for i, panel in enumerate(panels):
        b[i] = -V * np.cos(a - panel.delta)
    # freestream contribution on the Kutta condition
    b[-1] = -V * (np.sin(a - panels[0].delta) +
                                 np.sin(a - panels[-1].delta) )
    return b

