import sympy as sym
import numpy as np

from sympy.solvers.solveset import linsolve

def solve_no_vortex(n, M, theta, V_val=None, alpha_val = None):
    # V inf
    V = sym.Symbol('V')
    # alpha
    a = sym.Symbol('a')
    # source
    q = sym.symbols('q_0:{}'.format(n))

    b = []
    for i in range(n):
        temp = -V * sym.sin(a - theta[i])
        if V_val and alpha_val:
            temp = temp.subs([(V, V_val), (a, alpha_val)])
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
