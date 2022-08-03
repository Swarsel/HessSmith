import matplotlib

from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from external.AngleAnnotation import AngleAnnotation
import matplotlib.patches as patches

x,y = parsecoords("data/processeddata/naca0012b.dat")
panels = define_panels(x,y)
for panel in panels:
    print(panel)
profile = AirfoilProfile(panels, vortex=True)
profile.solve()
print(profile)