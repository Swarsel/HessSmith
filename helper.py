import numpy as np
from numpy import sqrt
from math import atan2

def index(list: list, element: int) -> float:
    # allows to use normal list as a closed loop, connecting the last and first elements
    return list[element % len(list)]

def parsecoords(filename: str) -> list:
    # reads coordinates from file
    parsed = np.loadtxt(filename, unpack=True)
    return [(parsed[0][i], parsed[1][i]) for i in range(len(parsed[0]))]

def split_xy(coords: list) -> (list, list):
    # splits a list of coordinates into x & y
    return [coords[i][0] for i in range(len(coords))],\
           [coords[i][1] for i in range(len(coords))]

def preprocess_list_header(filename):
    with open("data/rawestdata/" + filename) as file:
        with open ("data/rawedata/" + filename, "w+") as write:
            for line in file:
                if any(char.isalpha() for char in line):
                    continue
                else:
                    write.write(line)

def preprocess_list_n(filename):
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

def split_data(filename):
    # splits data in first half of loop and other half (which needs to be reversed)
    with open("data/rawdata/" + filename) as file:
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

def merge_and_reverse_lists (filename):
    # merge two lists and reverse the second one
    with open("data/loopdata/" + filename[:-4] + "_loop.dat", "w+") as write:
        with open("data/splitdata/" + filename[:-4] + "_1.dat", "r") as file:
            for line in file:
                write.write(line)
        with open("data/splitdata/" + filename[:-4] + "_2.dat", "r") as file:
            lines = []
            for line in file:
                lines.append(line)
            lines.reverse()
            for line in lines:
                write.write(line)

def make_continuuous_loop(filename):
    preprocess_list_header(filename)
    preprocess_list_n(filename)
    split_data(filename)
    merge_and_reverse_lists(filename)

def compute_vals(x,y):
    n = len(x)
    # calculate middle points
    X, Y = [], []
    for i in range(n):
        X.append(round((index(x, -i) + index(x, -i - 1)) / 2, 4))
        Y.append(round((index(y, -i) + index(y, -i - 1)) / 2, 4))

    # calculate angle of panel
    theta = []
    for i in range(n):
        theta.append(atan2(index(y, -i - 1) - index(y, -i),
                           index(x, -i - 1) - index(x, -i)))

    # calculate panel length
    l = []
    for i in range(n):
        l.append(sqrt((index(x, -i - 1) - index(x, -i)) ** 2 +
                      (index(y, -i - 1) - index(y, -i)) ** 2))

    return X, Y, theta, l

def compute_circumference(x, y):
    n = len(x)
    # calculate circumference
    U = sum([sqrt((index(x, i + 1) - index(x, i)) ** 2 +
                  (index(y, i + 1) - index(y, i)) ** 2) for i in range(n)])
    return U

def compute_xi_eta(n, X, Y, theta):
    xi = np.zeros((n, n))
    eta = np.zeros((n, n))

    for i in range(n):
        for j in range(n):
            xi[i][j] = (X[i] - X[j]) * np.cos(theta[j]) + (Y[i] - Y[j]) * np.sin(theta[j])
            eta[i][j] = -(X[i] - X[j]) * np.sin(theta[j]) + (Y[i] - Y[j]) * np.cos(theta[j])
    return xi, eta

def compute_I_J(n, l, xi, eta):
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
                J[i][j] = 1 / (2 * np.pi) * atan2(l[j] - 2 * xi[i][j], 2 * eta[i][j]) + 1 / \
                          (2 * np.pi) * atan2(l[j] + 2 * xi[i][j], 2 * eta[i][j])
    return I, J

def compute_An_M(n, theta, I, J):
    M = np.zeros((n, n))
    A_n = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A_n[i][j] = - np.sin(theta[i] - theta[j]) * I[i][j] + np.cos(theta[i] - theta[j]) * J[i][j]
            M[i][j] = A_n[i][j]
    return A_n, M

def compute_At(n, theta, I, J):
    A_t = np.zeros((n, n))
    for i in range(n):
        for j in range(n):
            A_t[i][j] = np.cos(theta[i] - theta[j]) * I[i][j] + np.sin(theta[i] - theta[j]) * J[i][j]
    return A_t