import sympy as sym
from helper import compute_vals, compute_xi_eta, compute_I_J, compute_An_M, compute_updrift, compute_At, compute_cp, compute_vt_vortex
from make_cylinder import cylinder
from sympy.solvers.solveset import linsolve
import numpy as np
from solving import solve_vortex

V=1
a=10
t=1
for panels in range(8,9):
    x, y = cylinder(n = panels)
    n = len(x)
    X, Y, theta, l = compute_vals(x,y)
    xi, eta = compute_xi_eta(n, X, Y, theta)
    I, J = compute_I_J(n, l, xi, eta)
    A_n, M = compute_An_M(n , theta, I, J)
    A_t = compute_At(n, theta, I, J)

    # source
    q = sym.symbols('q_0:{}'.format(n+1))

    q_sol = solve_vortex(n, M, A_t, A_n, theta, V=V, a=a)
    # tangential component of velocity

    vt = compute_vt_vortex(n, A_t, A_n, theta, q_sol, V=V, a=a)

    # constituent pressure
    cp = compute_cp(n, vt, V=V)

    # constituent updrift
    ca = compute_updrift(n, vt, l, V=V, t=t)

    print(f"Panels: {panels} \n"
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