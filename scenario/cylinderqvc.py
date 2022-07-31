from make_cylinder import cylinder, circle
from helper import make_panels
from profile_new import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot
import sympy as sym
from sympy import Number
from sympy.solvers.solveset import linsolve


def cylinderqvc():
    x,y,_ = cylinder(n=8)
    panels = make_panels(x,y)
    profile = AirfoilProfile(panels,vortex=False)
    profile.solve(V=1,a=0)
    with open("data/scenarios/cylinderqvc/cylinderqvc.txt", "w+") as write:
        for panel in profile.panels:
            txt = str(round(panel.q,2)) + " & " + str(round(panel.vt,2)) + " & " + str(round(panel.cp,2)) + "\\\\ \n"
            write.write(txt)