from computations import compute_vals, compute_system
from make_cylinder import cylinder

x, y = cylinder()
n = len(x)
X, Y, theta, l = compute_vals(x,y)

xi, eta, I, J, A_n, A_t, M = compute_system(n, X, Y, theta, l)

print(M)
