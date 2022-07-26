from make_cylinder import cylinder
from solving import solve_no_vortex
from computations import compute_vals, compute_system, compute_vt, compute_cp

for panels in range(6, 12):
    x, y = cylinder(n=panels)
    n = len(x)
    X, Y, theta, l = compute_vals(x, y)
    xi, eta, I, J, A_n, A_t, M = compute_system(n, X, Y, theta, l)

    # solution

    # q_sol = solve_no_vortex(n,M, theta, V=1, a=10)
    q_sol = solve_no_vortex(n, M, theta)

    # tangential component of velocity

    # vt = compute_vt(n, A_t, theta, q_sol, V=1, a=10)
    vt = compute_vt(n, A_t, theta, q_sol)

    # constituent pressure

    # cp = compute_cp(n, vt, V=1)
    cp = compute_cp(n, vt)

    print(f"Panels: {panels}\n"
          f"Tangential velocity:\n"
          f"{vt}\n"
          f"Constituent Pressure:\n"
          f"{cp}\n\n")
