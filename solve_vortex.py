import sympy as sym
from make_cylinder import cylinder
from solving import solve_vortex
from computations import compute_vals, compute_system, compute_vt_vortex, compute_cp, compute_updrift

# constants
V = 1
a = 10
t = 1

for panels in range(8, 9):
    x, y = cylinder(n=panels)
    n = len(x)
    X, Y, theta, l = compute_vals(x, y)
    xi, eta, I, J, A_n, A_t, M = compute_system(n, X, Y, theta, l)

    # solution

    # q_sol = solve_vortex(n, M, A_t, A_n, theta, V=V, a=a)
    q_sol = solve_vortex(n, M, A_t, A_n, theta)

    # tangential component of velocity

    # vt = compute_vt_vortex(n, A_t, A_n, theta, q_sol, V=V, a=a)
    vt = compute_vt_vortex(n, A_t, A_n, theta, q_sol)

    # constituent pressure

    # cp = compute_cp(n, vt, V=V)
    cp = compute_cp(n, vt)

    # constituent updrift

    # ca = compute_updrift(n, vt, l, V=V, t=t)
    ca = compute_updrift(n, vt, l)

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
