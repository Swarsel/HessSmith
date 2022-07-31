from make_cylinder import cylinder, circle
from helper import make_panels
from profile_new import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot
import sympy as sym
from sympy import Number
from sympy.solvers.solveset import linsolve

def rotatingcylinder():
    with open("data/scenarios/rotatingcylinder/rotatingcylinder.txt", "w+") as write:
        x,y,_ = cylinder(n=8)
        panels = make_panels(x,y)
        profile = AirfoilProfile(panels,vortex=True)
        for a in range(-15,16):
            profile.solve(V=1, a=a)
            txt = str(a) + " & " + str(round(profile.gamma,2)) + " & " + str(round(profile.ca,2)) + " & "
            for panel in profile.panels:
                txt += str(round(panel.cp, 2)) + " & "
            write.write(txt[:-2] + "\\\\ \n")

