from solving import solve_vortex_np
from computations import compute_cp, compute_updrift, compute_vt_vortex
from sympy import Symbol


def hess_smith(n, theta, l, A_n, A_t, M, V=Symbol("V"), a=Symbol("a"), t=Symbol("t")):
    q_sol = solve_vortex_np(n, M, A_t, A_n, theta, V, a)
    vt = compute_vt_vortex(n, A_t, A_n, theta, q_sol, V, a)
    cp = compute_cp(n, vt, V)
    gamma = q_sol[-1]
    ca = compute_updrift(n, vt, l, V, t)
    return q_sol, gamma, vt, cp, ca