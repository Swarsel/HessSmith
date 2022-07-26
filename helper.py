import numpy as np
from numpy import sqrt
from math import atan2
import sympy as sym


def index(list: list, element: int) -> float:
    # allows to use normal list as a closed loop, connecting the last and first elements
    return list[element % len(list)]


def parsecoords(filename: str) -> list:
    # reads coordinates from file
    parsed = np.loadtxt(filename, unpack=True)
    return [(parsed[0][i], parsed[1][i]) for i in range(len(parsed[0]))]


def split_xy(coords: list) -> (list, list):
    # splits a list of coordinates into x & y
    return [coords[i][0] for i in range(len(coords))], \
           [coords[i][1] for i in range(len(coords))]


def preprocess_list(filename: str) -> None:
    with open("data/rawdata/" + filename) as file:
        with open("data/skinneddata/" + filename, "w+") as write:
            for line in file:
                if any(char.isalpha() for char in line):
                    continue
                else:
                    s = line.strip().split(".")
                    try:
                        if int(s[0]) > 1:
                            continue
                    except:
                        pass
                    write.write(line)


def check_selig_format(filename: str) -> bool:
    with open("data/skinneddata/" + filename) as file:
        for line in file:
            s = line.strip().split(".")
            try:
                if int(s[0]) == 1:
                    return True
                elif int(s[0]) == 0:
                    return False
            except:
                pass
            break


'''
def preprocess_list_n(filename: str) -> None:
    with open("data/rawedata/" + filename) as file:
        with open("data/rawdata/" + filename, "w+") as write:
            for line in file:
                s = line.strip().split(".")
                try:
                    if int(s[0]) > 1:
                        continue
                except:
                    pass
                write.write(line)
'''


def split_data(filename: str) -> None:
    # splits data in first half of loop and other half (which needs to be reversed)
    with open("data/skinneddata/" + filename) as file:
        with open("data/splitdata/" + filename[:-4] + "_1.dat", "w+") as write1:
            with open("data/splitdata/" + filename[:-4] + "_2.dat", "w+") as write2:
                flag = False
                count = 0
                for line in file:
                    if any(char.isdigit() for char in line) and not flag:
                        write1.write(line)
                    elif any(char.isdigit() for char in line) and flag:
                        write2.write(line)
                    elif count != 0:
                        flag = True
                    count += 1


def merge_and_reverse_lists(filename: str, rev1=True, rev2=False) -> str:
    # merge two lists and reverse the second one
    with open("data/loopdata/" + filename, "w+") as write:
        with open("data/splitdata/" + filename[:-4] + "_1.dat", "r") as file:
            lines1 = []
            for line in file:
                lines1.append(line)
            if rev1:
                lines1.reverse()
            for line in lines1:
                write.write(line)
        with open("data/splitdata/" + filename[:-4] + "_2.dat", "r") as file:
            lines2 = []
            for line in file:
                lines2.append(line)
            if rev2:
                lines2.reverse()
            for line in lines2:
                write.write(line)


def finish_data(filename, path):
    with open("data/processeddata/" + filename, "w+") as write:
        with open(path + filename) as file:
            for line in file:
                write.write(line)


def make_continuuous_loop(filename: str, rev1=True, rev2=False) -> None:
    preprocess_list(filename)
    # preprocess_list_n(filename)
    selig = check_selig_format(filename)
    if not selig:
        split_data(filename)
        merge_and_reverse_lists(filename, rev1, rev2)
        finish_data(filename, "data/loopdata/")
    else:
        finish_data(filename, "data/skinneddata/")


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


def compute_xi_eta(n: int, X: list, Y: list, theta: list):
    xi = np.zeros((n, n))
    eta = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            xi[i][j] = (X[i] - X[j]) * np.cos(theta[j]) + (Y[i] - Y[j]) * np.sin(theta[j])
            eta[i][j] = -(X[i] - X[j]) * np.sin(theta[j]) + (Y[i] - Y[j]) * np.cos(theta[j])
    return xi, eta


def compute_I_J(n: int, l: list, xi, eta):
    I = np.zeros((n, n))
    J = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            if i == j:
                I[i][j] = 0
                J[i][j] = 0.5
            else:
                I[i][j] = 1 / (4 * np.pi) * np.log(((l[j] + 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2) /
                                                   ((l[j] - 2 * xi[i][j]) ** 2 + 4 * eta[i][j] ** 2))
                J[i][j] = 1 / (2 * np.pi) * atan2(l[j] - 2 * xi[i][j], 2 * eta[i][j]) + \
                          1 / (2 * np.pi) * atan2(l[j] + 2 * xi[i][j], 2 * eta[i][j])
    return I, J


def compute_An_M(n: int, theta: list, I, J):
    M = np.zeros((n, n))
    A_n = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A_n[i][j] = - np.sin(theta[i] - theta[j]) * I[i][j] + np.cos(theta[i] - theta[j]) * J[i][j]
            M[i][j] = A_n[i][j]
    return A_n, M


def compute_At(n: int, theta: int, I, J):
    A_t = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A_t[i][j] = np.cos(theta[i] - theta[j]) * I[i][j] + np.sin(theta[i] - theta[j]) * J[i][j]
    return A_t


def compute_vt(n, A_t, theta, q_sol, V=sym.Symbol("V"), a=sym.Symbol("a")):
    vt = []
    for i in range(n):
        vt.append(sum([A_t[i][j] * q_sol[j] for j in range(n)]) + V * sym.cos(a - theta[i]))
    return vt

def compute_vt_vortex(n, A_t, A_n, theta, q_sol, V=sym.Symbol("V"), a=sym.Symbol("a")):
    vt = []
    for i in range(n):
        vt.append(
            sum([A_t[i][j] * q_sol[j] for j in range(n)]) - q_sol[n] * sum([A_n[i][j] for j in range(n)]) + V * sym.cos(
                a - theta[i]))
    return vt


def compute_cp(n, vt, V=sym.Symbol("V")):
    cp = []
    for i in range(n):
        cp.append(1 - (vt[i] / V) ** 2)
    return cp

def compute_updrift(n, vt, l, V=sym.Symbol("V"), t=sym.Symbol("t")):
    # constituent updrift7
    ca = 2 / (V * t) * sum([vt[i] * l[i] for i in range(n)])
    return ca
