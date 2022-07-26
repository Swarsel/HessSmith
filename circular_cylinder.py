import sympy as sym
from helper import compute_vals, compute_xi_eta, compute_I_J, compute_An_M, compute_At, compute_vt
from make_cylinder import cylinder
from sympy.solvers.solveset import linsolve

for panels in range(6,12):
    x, y = cylinder(n = panels)
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

    # tangential component of velocity
    A_t = compute_At(n, theta, I, J)
    '''
    vt = []
    for i in range(n):
        vt.append(sum([A_t[i][j] * q_sol[j] for j in range(n)]) + V * sym.cos(a - theta[i]))
    '''
    vt = compute_vt(n, A_t, theta, q_sol)

    # constituent pressure
    cp = []
    for i in range(n):
        cp.append(1 - (vt[i] / V)**2)

    print(f"Panels: {panels}\n"
          f"Tangential velocity:\n"
          f"{vt}\n"
          f"Constituent Pressure:\n"
          f"{cp}\n\n")

