import sympy as sym
from helper import compute_vals, compute_xi_eta, compute_I_J, compute_An_M
from solving import solve_no_vortex
from make_cylinder import cylinder
from sympy.solvers.solveset import linsolve
x, y = cylinder()
n = len(x)
X, Y, theta, l = compute_vals(x,y)
xi, eta = compute_xi_eta(n, X, Y, theta)
I, J = compute_I_J(n, l, xi, eta)
A_n, M = compute_An_M(n , theta, I, J)

q_sol = solve_no_vortex(n, M, theta)

sum_sol = sum([q_sol[i] * l[i] for i in range(n)])
print(q_sol)