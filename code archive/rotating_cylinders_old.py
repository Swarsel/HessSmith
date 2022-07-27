from hess_smith import hess_smith
from computations import compute_vals, compute_system
from make_cylinder import cylinder

for panels in range(6, 12):
    for a in range(0, 360):
        x, y = cylinder(n=panels)
        n = len(x)
        X, Y, theta, l = compute_vals(x, y)
        xi, eta, I, J, A_n, A_t, M = compute_system(n, X, Y, theta, l)

        q_sol, gamma, vt, cp, ca = hess_smith(n, theta, l, A_n, A_t, M, a=a)

        print(f"Panels: {panels}, Angle: {a}\n"
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