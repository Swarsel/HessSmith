from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def novortexsystemmatrix():
    x, y, _ = cylinder(n=8)
    panels = make_panels(x,y)
    profile = AirfoilProfile(panels,vortex=False)
    print(profile.M)
    with open("data/scenarios/novortexsystemmatrix/novortexsystemmatrix.txt", "w+") as write:
        for row in profile.M:
            txt = ""
            for item in row:
                txt += str(round(item,3)) + "&"
            write.write(txt[:-1] + "\\\\ \n")