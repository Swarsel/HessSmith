import sympy as sym
from helper import compute_vals, compute_xi_eta, compute_I_J, compute_An_M, compute_At
from make_cylinder import cylinder
from sympy.solvers.solveset import linsolve
import numpy as np

for panels in [8]:
    x, y = cylinder(na = panels)
    n = len(x)
    X, Y, theta, l = compute_vals(x,y)
    xi, eta = compute_xi_eta(n, X, Y, theta)
    I, J = compute_I_J(n, l, xi, eta)
    A_n, M = compute_An_M(n , theta, I, J)
    A_t = compute_At(n, theta, I, J)

    # V inf
    V = sym.Symbol('V')

    # alpha
    a = sym.Symbol('a')

    # source
    q = sym.symbols('q_0:{}'.format(n+1))

    # calculate inhomogenous terms
    b = []
    for i in range(n):
        b.append(-V * sym.sin(a - theta[i]))


    # resize M for vortex
    nh = np.zeros((n,1))
    nv = np.zeros((1, n + 1))
    M = np.hstack((M,nh))
    M = np.vstack((M,nv))

    for i in range(n):
        M[i][n] = sum([A_t[i][j] for j in range(n)])
        M[n][i] = A_t[0][i] + A_t[n-1][i]
    M[n][n] = - sum([A_n[0][j] + A_n[n-1][j] for j in range(n)])

    b.append(-V * (sym.cos(a-theta[0]) + sym.cos(a - theta[n-1])))

    # gamma
    g = sym.Symbol("g")

    eq = []
    for i in range(n):
        eq.append(sum([M[i][j] * q[j] for j in range(n)]) - b[i])
    eq.append(sum([M[n][j] * q[j] for j in range(n+1)]) - b[n])

    q_s = list(linsolve(eq, q))
    # solution vector
    q_sol = []
    for c in q_s[0]:
        q_sol.append(c)

    # tangential component of velocity

    vt = []
    for i in range(n):
        vt.append(sum([A_t[i][j] * q_sol[j] for j in range(n)]) - q[n] * sum([A_n[i][j] for j in range(n)]) + V * sym.cos(a - theta[i]))

    # constituent pressure
    cp = []
    for i in range(n):
        cp.append(1 - (vt[i] / V) ** 2)

    # depth
    t = sym.Symbol("t")

    # constituent updrift
    ca = 2/(V*t) * sum([vt[i] * l[i] for i in range(n)])

    print(f"Panels: {panels}\n"
          f"Tangential velocity:\n"
          f"{vt}\n"
          f"Constituent Pressure:\n"
          f"{cp}\n"
          f"Source vector:\n"
          f"{q_sol}\n"
          f"Gamma:\n"
          f"{q_sol[n]}\n"
          f"Constituent updrift:\n"
          f"{ca}\n\n")