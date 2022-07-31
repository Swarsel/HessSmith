from make_cylinder import cylinder, circle
from helper import make_panels, write_coords
from profile import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot
from sympy.solvers.solveset import linsolve
import sympy as sym
from sympy import Number

x, y = cylinder(n=8)
panels = make_panels(x, y)
profile = AirfoilProfile(panels, f"Sided Cylinder", vortex=False)
n = len(x)-1
print(n)

M = [[0.5, 0.05615476, 0.06394829, 0.06483409, 0.06500511, 0.06483409, 0.06394829, 0.05615476],
     [0.05615476, 0.5, 0.05615476, 0.06394829, 0.06483409, 0.06500511, 0.06483409, 0.06394829],
     [0.06394829, 0.05615476, 0.5, 0.05615476, 0.06394829, 0.06483409, 0.06500511, 0.06483409],
     [0.06483409, 0.06394829, 0.05615476, 0.5, 0.05615476, 0.06394829, 0.06483409, 0.06500511],
     [0.06500511, 0.06483409, 0.06394829, 0.05615476, 0.5, 0.05615476, 0.06394829, 0.06483409],
     [0.06483409, 0.06500511, 0.06483409, 0.06394829, 0.05615476, 0.5, 0.05615476, 0.06394829],
     [0.06394829, 0.06483409, 0.06500511, 0.06483409, 0.06394829, 0.05615476, 0.5, 0.05615476],
     [0.05615476, 0.06394829, 0.06483409, 0.06500511, 0.06483409, 0.06394829, 0.05615476, 0.5]]

def compute_inhomogenity(panels, vortex, V=sym.Symbol("V"), a=sym.Symbol("a")):
    if vortex:
        b = []
    else:
        b = []
    for i, panel in enumerate(panels):
        b.append(V * sym.sin(a - panel.theta))
    # b_n
    if vortex:
        b[-1] = -V * (sym.cos(a - panels[0].theta) + sym.cos(a - panels[-1].theta))
    return b

b = compute_inhomogenity(panels,vortex=False)

# source
q = sym.symbols('q_0:{}'.format(n))

from sympy.core.rules import Transform
eq = []
for i in range(n):
    eq.append(sum([M[i][j] * q[j] for j in range(n)]) - b[i])

def round_expr(expr, num_digits):
    return expr.xreplace({n : round(n, num_digits) for n in expr.atoms(Number)})
q_s = list(linsolve(eq, q))
# solution vector
q_sol = []
for c in q_s[0]:
    q_sol.append(c)
a = []
for q in q_sol:
    a.append(round_expr(q,2))
print(a)