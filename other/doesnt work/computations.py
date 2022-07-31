import numpy as np
from math import atan2


def compute_xi(n: int, panels):
    xi = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            xi[i][j] = (panels[i].xm - panels[j].xm) * np.cos(panels[j].theta) + (panels[i].ym - panels[j].ym) * np.sin(
                panels[j].theta)
    return xi


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


def compute_I_free(n: int, plen, xi, eta, panels):
    I = np.empty((n, plen))
    for i in range(n):
        for j in range(plen):
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
             #   A_n[i][j] = np.sin(panels[i].theta - panels[j].theta) * I[i][j] - np.cos(
              #      panels[i].theta - panels[j].theta) * J[i][j]
    return A_n


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
