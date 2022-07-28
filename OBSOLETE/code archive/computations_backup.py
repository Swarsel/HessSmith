import numpy as np
from numpy import sqrt
from math import atan2
import sympy as sym
from helper import index


def compute_vals(x: list, y: list) -> (list, list, list, list):
    n = len(x)

    # calculate middle points
    X, Y = [], []
    for i in range(n):
        X.append(round((index(x, n - i) + index(x, n - i - 1)) / 2, 4))
        Y.append(round((index(y, n - i) + index(y, n - i - 1)) / 2, 4))

    # calculate angle of panel
    theta = []
    for i in range(n):
        theta.append(atan2(index(y, n - i - 1) - index(y, n - i),
                           index(x, n - i - 1) - index(x, n - i)))

    # calculate panel length
    l = []
    for i in range(n):
        l.append(sqrt((index(x, n - i - 1) - index(x, n - i)) ** 2 +
                      (index(y, n - i - 1) - index(y, n - i)) ** 2))

    return X, Y, theta, l

def compute_circumference(x: list, y: list) -> float:
    n = len(x)
    # calculate circumference
    U = sum([sqrt((index(x, i + 1) - index(x, i)) ** 2 +
                  (index(y, i + 1) - index(y, i)) ** 2) for i in range(n)])
    return U

def compute_circumference_n(panels) -> float:
    # calculate circumference
    U = sum([sqrt((panel.xb - panel.xa) ** 2 +
                  (panel.yb - panel.ya) ** 2) for panel in panels])
    return U


def compute_xi_old(n: int, X: list, Y: list, theta: list):
    xi = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            xi[i][j] = (X[i] - X[j]) * np.cos(theta[j]) + (Y[i] - Y[j]) * np.sin(theta[j])
    return xi

def compute_xi(n: int, panels):
    xi = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            xi[i][j] = (panels[i].xm - panels[j].xm) * np.cos(panels[j].theta) + (panels[i].ym - panels[j].ym) * np.sin(panels[j].theta)
    return xi


def compute_eta_old(n: int, X: list, Y: list, theta: list):
    eta = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            eta[i][j] = -(X[i] - X[j]) * np.sin(theta[j]) + (Y[i] - Y[j]) * np.cos(theta[j])
    return eta

def compute_eta(n: int, panels):
    eta = np.empty((n, n))

    for i in range(n):
        for j in range(n):
            eta[i][j] = -(panels[i].xm - panels[j].xm) * np.sin(panels[j].theta) + (panels[i].ym - panels[j].ym) * np.cos(panels[j].theta)
    return eta


def compute_I_old(n: int, l: list, xi, eta):
    I = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                I[i][j] = 0
            else:
                I[i][j] = 1 / (4 * np.pi) * np.log(((l[j] + 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2) /
                                                   ((l[j] - 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2))
    return I

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


def compute_J_old(n: int, l: list, xi, eta):
    J = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                J[i][j] = 0.5
            else:
                J[i][j] = 1 / (2 * np.pi) * atan2(l[j] - 2 * xi[i][j], 2 * eta[i][j]) + \
                          1 / (2 * np.pi) * atan2(l[j] + 2 * xi[i][j], 2 * eta[i][j])
    return J

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


def compute_An_old(n: int, theta: list, I, J):
    A_n = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            A_n[i][j] = - np.sin(theta[i] - theta[j]) * I[i][j] + np.cos(theta[i] - theta[j]) * J[i][j]
    return A_n

def compute_An(n: int, I, J, panels):
    A_n = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            A_n[i][j] = - np.sin(panels[i].theta - panels[j].theta) * I[i][j] + np.cos(panels[i].theta - panels[j].theta) * J[i][j]
    return A_n


def compute_At_old(n: int, theta: list, I, J):
    A_t = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            A_t[i][j] = np.cos(theta[i] - theta[j]) * I[i][j] + np.sin(theta[i] - theta[j]) * J[i][j]
    return A_t

def compute_At(n: int, I, J, panels):
    A_t = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            A_t[i][j] = np.cos(panels[i].theta - panels[j].theta) * I[i][j] + np.sin(panels[i].theta - panels[j].theta) * J[i][j]
    return A_t


def compute_M(n: int, A_n):
    M = np.empty((n, n))
    for i in range(n):
        for j in range(n):
            M[i][j] = A_n[i][j]
    return M


def compute_system(n: int, X: list, Y: list, theta: list, l: list):
    # compute system parameters
    xi = compute_xi_old(n, X, Y, theta)
    eta = compute_eta_old(n, X, Y, theta)
    I = compute_I_old(n, l, xi, eta)
    J = compute_J_old(n, l, xi, eta)
    A_n = compute_An_old(n, theta, I, J)
    A_t = compute_At_old(n, theta, I, J)
    M = compute_M(n, A_n)
    return xi, eta, I, J, A_n, A_t, M


def compute_vt(n, A_t, theta, q_sol, V=sym.Symbol("V"), a=sym.Symbol("a")):
    # tangential velocity without vortex
    vt = []
    for i in range(n):
        vt.append(sum([A_t[i][j] * q_sol[j] for j in range(n)]) + V * sym.cos(a - theta[i]))
    return vt


def compute_vt_vortex(n, A_t, A_n, theta, q_sol, V=sym.Symbol("V"), a=sym.Symbol("a")):
    # tangential velocity under vortex
    vt = []
    for i in range(n):
        vt.append(
            sum([A_t[i][j] * q_sol[j] for j in range(n)]) - q_sol[n] * sum([A_n[i][j] for j in range(n)]) + V * sym.cos(
                a - theta[i]))
    return vt


def compute_cp(n, vt, V=sym.Symbol("V")):
    # constituent pressure
    cp = []
    for i in range(n):
        cp.append(1 - (vt[i] / V) ** 2)
    return cp


def compute_updrift(n, vt, l, V=sym.Symbol("V"), t=sym.Symbol("t")):
    # constituent updrift
    ca = 2 / (V * t) * sum([vt[i] * l[i] for i in range(n)])
    return ca

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

def compute_inhomogenity(panels, V, a):
    b = np.empty(panels.size + 1, dtype=float)
    for i, panel in enumerate(panels):
        b[i] = -V * np.sin(a - panels[i].theta)
    # b_n
    b[-1] = -V * (np.cos(a - panels[0].theta) + np.cos(a - panels[-1].theta))
    return b

'''
def compute_inhomogenity(panels, V, a):

    b = np.empty(panels.size + 1, dtype=float)
    # freestream contribution on each panel
    for i, panel in enumerate(panels):
        b[i] = -V * np.cos(a - panel.theta)
    # freestream contribution on the Kutta condition
    b[-1] = -V * (np.sin(a - panels[0].theta) +
                                 np.sin(a - panels[-1].theta))
    return b
'''
