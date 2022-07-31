from make_cylinder import cylinder, circle
from helper import make_panels, parsecoords,define_panels
from profile_new import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
from sympy import Number
from sympy.solvers.solveset import linsolve
import os

def naca0012():
    x,y = parsecoords("data/processeddata/naca0012b.dat")
    panels = define_panels(x,y)
    profile = AirfoilProfile(panels, vortex=True)
    profile.solve(a=5)
    print(profile)

naca0012()