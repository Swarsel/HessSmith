from helper import compute_vals, compute_xi_eta, compute_I_J, compute_An_M
from make_cylinder import cylinder

x, y = cylinder()
n = len(x)
X, Y, theta, l = compute_vals(x,y)

xi, eta = compute_xi_eta(n, X, Y, theta)
I, J = compute_I_J(n, l, xi, eta)

A_n, M = compute_An_M(n, theta, I, J)

print(M)
