import sympy as sym
import numpy as np
from computations import system_matrix

from sympy.solvers.solveset import linsolve

def solve_no_vortex(n, M, theta, V=sym.Symbol("V"), a=sym.Symbol("a")):

    # source
    q = sym.symbols('q_0:{}'.format(n))

    b = []
    for i in range(n):
        temp = -V * sym.sin(a - theta[i])
        b.append(temp)

    eq = []
    for i in range(n):
        eq.append(sum([M[i][j] * q[j] for j in range(n)]) - b[i])

    q_s = list(linsolve(eq, q))
    # solution vector
    q_sol = []
    for c in q_s[0]:
        q_sol.append(c)
    return q_sol

def solve_vortex(n, M, A_t, A_n, theta, V=sym.Symbol("V"), a=sym.Symbol("a")):

    # source
    q = sym.symbols('q_0:{}'.format(n+1))

    # calculate inhomogenous terms
    b = []
    for i in range(n):
        temp = -V * sym.sin(a - theta[i])
        b.append(temp)

    # resize M for vortex
    nh = np.zeros((n, 1))
    nv = np.zeros((1, n + 1))
    M = np.hstack((M, nh))
    M = np.vstack((M, nv))

    for i in range(n):
        M[i][n] = sum([A_t[i][j] for j in range(n)])
        M[n][i] = A_t[0][i] + A_t[n - 1][i]
    M[n][n] = - sum([A_n[0][j] + A_n[n - 1][j] for j in range(n)])

    #b_n
    temp = -V * (sym.cos(a - theta[0]) + sym.cos(a - theta[n - 1]))
    b.append(temp)

    eq = []
    for i in range(n+1):
        eq.append(sum([M[i][j] * q[j] for j in range(n+1)]) - b[i])

    q_s = list(linsolve(eq, q))
    # solution vector
    q_sol = []
    for c in q_s[0]:
        q_sol.append(c)

    return q_sol

def solve_vortex_np(n, M, A_t, A_n, theta, V=1, a=0):


    # calculate inhomogenous terms
    ''''''
    b = []
    for i in range(n):
        temp = -V * np.sin(a - theta[i])
        b.append(temp)
    '''
    # resize M for vortex
    nh = np.empty((n, 1))
    nv = np.empty((1, n + 1))
    M = np.hstack((M, nh))
    M = np.vstack((M, nv))

    for i in range(n):
        M[i][n] = sum([A_t[i][j] for j in range(n)])
        M[n][i] = A_t[0][i] + A_t[n - 1][i]
    M[n][n] = - sum([A_n[0][j] + A_n[n - 1][j] for j in range(n)])
    '''
    M = system_matrix(A_n, A_t)

    #b_n
    temp = -V * (np.cos(a - theta[0]) + np.cos(a - theta[n - 1]))
    b.append(temp)
    b = np.array(b)

    '''
    eq = []
    for i in range(n+1):
        eq.append(sum([M[i][j] * q[j] for j in range(n+1)]) - b[i])
    '''
    q_s = np.linalg.solve(M,b)
    # solution vector
    q_sol =[]
    for i in range(len(q_s)):
        q_sol.append(q_s[i])

    return q_sol
