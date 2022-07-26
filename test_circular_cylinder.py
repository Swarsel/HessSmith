import sympy as sym
from helper import compute_vals, compute_xi_eta, compute_I_J, compute_An_M, compute_At, compute_vt, compute_cp
from make_cylinder import cylinder
from sympy.solvers.solveset import linsolve
from solving import solve_no_vortex

for panels in range(6,12):
    x, y = cylinder(n = panels)
    n = len(x)
    X, Y, theta, l = compute_vals(x,y)
    xi, eta = compute_xi_eta(n, X, Y, theta)
    I, J = compute_I_J(n, l, xi, eta)
    A_n, M = compute_An_M(n , theta, I, J)

    q_sol = solve_no_vortex(n,M, theta, V_val=1, alpha_val=10)

    # tangential component of velocity
    A_t = compute_At(n, theta, I, J)
    vt = compute_vt(n, A_t, theta, q_sol, V=1, a=10)

    # constituent pressure
    cp = compute_cp(n, vt, V=1)

    print(f"Panels: {panels}\n"
          f"Tangential velocity:\n"
          f"{vt}\n"
          f"Constituent Pressure:\n"
          f"{cp}\n\n")

