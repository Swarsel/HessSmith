from make_cylinder import cylinder, circle
from helper import make_panels
from profile_new import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot
import sympy as sym
from sympy import Number
from sympy.solvers.solveset import linsolve

def compute_inhomogenity_here(n, panels, vortex, V=sym.Symbol("V"), a=sym.Symbol("a")):
    t = sym.symbols('t_0:{}'.format(n))
    if vortex:
        b = []
    else:
        b = []
    for i in range(n):
        b.append(V * sym.sin(a - t[i]))
    # b_n
    if vortex:
        b[-1] = -V * (sym.cos(a - panels[0].theta) + sym.cos(a - panels[-1].theta))
    return b

def analyticalcylinder():
    x, y,_ = cylinder(n=8)
    panels = make_panels(x, y)
    profile = AirfoilProfile(panels, f"Sided Cylinder", vortex=False)
    n = len(x) - 1
    print(n)
    m = n-1
    M0 = sym.symbols('M_0_0:{}'.format(n))
    M1 = sym.symbols('M_1_0:{}'.format(n))
    M2 = sym.symbols('M_2_0:{}'.format(n))
    M3 = sym.symbols('M_3_0:{}'.format(n))
    M4 = sym.symbols('M_4_0:{}'.format(n))
    M5 = sym.symbols('M_5_0:{}'.format(n))
    M6 = sym.symbols('M_6_0:{}'.format(n))
    M7 = sym.symbols('M_7_0:{}'.format(n))
    M = [M0, M1, M2, M3, M4, M5, M6, M7]

    b = compute_inhomogenity_here(n,panels, vortex=False)

    # source
    q = sym.symbols('q_0:{}'.format(n))

    from sympy.core.rules import Transform
    eq = []
    for i in range(n):
        eq.append(sum([M[i][j] * q[j] for j in range(m)]) - b[i])

    def round_expr(expr, num_digits):
        return expr.xreplace({n: round(n, num_digits) for n in expr.atoms(Number)})

    q_s = list(linsolve(eq, q))
    # solution vector
    q_sol = []
    for c in q_s[0]:
        q_sol.append(c)
    a = []
    for q in q_sol:
        a.append(round_expr(q, 2))
    print(a)