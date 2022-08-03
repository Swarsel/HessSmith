import numpy as np
from math import atan2
from helper import ensure_zero

def compute_xi_free(plen, panels, x, y):
    xi = np.empty(plen)

    for j in range(plen):
        xi[j] = (x - panels[j].xm) * np.cos(panels[j].theta) + (y- panels[j].ym) * np.sin(
            panels[j].theta)
        xi[j] = ensure_zero(xi[j])
    return xi


def compute_eta_free(plen, panels, x, y):
    eta = np.empty(plen)

    for j in range(plen):
        eta[j] = -(x - panels[j].xm) * np.sin(panels[j].theta) + (
                y - panels[j].ym) * np.cos(panels[j].theta)
        eta[j] = ensure_zero(eta[j])
    return eta

def compute_I_free(plen, xi, eta, panels):
    I = np.empty(plen)
    for j in range(plen):
        #print("\n " + str(j))
        #print(panels[j].length)
        #print(xi[j])
        #print(eta[j])
        I[j] = 1 / (4 * np.pi) * np.log(((panels[j].length + 2 * xi[j]) ** 2 + 4 * eta[j] ** 2) /
                                               ((panels[j].length - 2 * xi[j]) ** 2 + 4 * eta[j] ** 2))
        I[j] = ensure_zero(I[j])
        #print(I[j])
        #print(panels[j].xm)
        #print(panels[j].ym)
    return I


def compute_J_free(plen, xi, eta, panels):
    J = np.empty(plen)
    for j in range(plen):
        J[j] = 1 / (2 * np.pi) * atan2(panels[j].length - 2 * xi[j], 2 * eta[j]) + \
                  1 / (2 * np.pi) * atan2(panels[j].length + 2 * xi[j], 2 * eta[j])
        J[j] = ensure_zero(J[j])
    return J

def compute_An_free(plen, I, J, panels):
    A_n = np.empty(plen)
    for j in range(plen):
        A_n[j] = - np.sin(- panels[j].theta) * I[j] + np.cos(
            - panels[j].theta) * J[j]
        A_n[j] = ensure_zero(A_n[j])
    return A_n


def compute_At_free(plen, I, J, panels):
    A_t = np.empty(plen)
    for j in range(plen):
        A_t[j] = np.cos(- panels[j].theta) * I[j] + np.sin(
            - panels[j].theta) * J[j]
        A_t[j] = ensure_zero(A_t[j])
    return A_t