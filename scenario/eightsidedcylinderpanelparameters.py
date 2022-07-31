from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def eightsidedcylinderpanelparameters():
    x, y, _ = cylinder(n=8)
    panels = make_panels(x, y)
    profile = AirfoilProfile(panels, name="8sidedcyl", vortex=False)
    profile.write_panels(filename="data/scenarios/eightsidedcylinderpanelparameters/eightsidedcylinderparameters.csv", n=2)
