import sympy as sym
from helper import compute_vals, compute_xi_eta, compute_I_J, compute_An_M, compute_At
from make_cylinder import cylinder
from sympy.solvers.solveset import linsolve
import numpy as np
x, y = cylinder()
n = len(x)
X, Y, theta, l = compute_vals(x,y)
xi, eta = compute_xi_eta(n, X, Y, theta)
I, J = compute_I_J(n, l, xi, eta)
A_n, M = compute_An_M(n , theta, I, J)

# V inf
V = sym.Symbol('V')

# alpha
a = sym.Symbol('a')

# source
q = sym.symbols('q_0:{}'.format(n))

# calculate inhomogenous terms
b = []
for i in range(n):
    b.append(-V * sym.sin(a - theta[i]))

eq = []
for i in range(n):
    eq.append(sum([M[i][j] * q[j] for j in range(n)]) - b[i])

q_s = list(linsolve(eq, q))
# solution vector
q_sol = []
for c in q_s[0]:
    q_sol.append(c)

sum_sol = sum([q_sol[i] * l[i] for i in range(n)])
print(sum_sol)
