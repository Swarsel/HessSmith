from computations import compute_vals, compute_system
from solving import solve_no_vortex
from make_cylinder import cylinder

x, y = cylinder()
n = len(x)
X, Y, theta, l = compute_vals(x, y)
xi, eta, I, J, A_n, A_t, M = compute_system(n, X, Y, theta, l)

q_sol = solve_no_vortex(n, M, theta)

sum_sol = sum([q_sol[i] * l[i] for i in range(n)])

print(f"Solution:\n"
      f"{q_sol}\n"
      f"Linear Combination:\n"
      f"{sum_sol}\n")