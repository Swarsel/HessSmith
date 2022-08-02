import matplotlib
import free
from helper import make_panels, parsecoords, define_panels, ensure_zero
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from external.AngleAnnotation import AngleAnnotation
import matplotlib.patches as patches

"""
x,y = parsecoords("data/processeddata/naca0012b.dat")

for rev in [True, False]:
    for dire in [True, False]:
        for flip in [True, False]:
            panels = define_panels(x,y, reverse=rev, dir=dire, flip=flip)
            profile = AirfoilProfile(panels, vortex=True)
            profile.solve(a=5)
            print(f"rev: {rev}, dir: {dire}, flip: {flip}: ca: {profile.ca}")
            #print(profile)
"""
"""
x= [1,0.5,0,0.5,1]
y= [0,0.5,0,-0.5,0]

panels = make_panels(x,y)
for panel in panels:
    print(panel)
profile = AirfoilProfile(panels)
profile.solve()
print(profile)
"""

x,y = parsecoords("data/processeddata/naca0012b.dat")


panels = define_panels(x,y)
profile = AirfoilProfile(panels, vortex=True)
profile.solve(a=5)
print(profile)

def vxvy(x,y, profile):
    eta = free.compute_eta_free(len(x), self.len, self.panels, x, y)
    xi = free.compute_xi_free(len(x), self.len, self.panels, x, y)
    I = free.compute_I_free(len(x), self.len, xi, eta, self.panels)
    J = free.compute_J_free(len(x), self.len, xi, eta, self.panels)
    An = free.compute_An_free(len(x), self.len, I, J, self.panels)
    At = free.compute_At_free(len(x), self.len, I, J, self.panels)
    vtx = sum([At[i][j] * profile.panels[j].q for j in range(profile.len)]) - profile.gamma * sum(
        [An[i][j] for j in range(profile.len)]) + V * np.cos(a)

    vty = sum([An[i][j] * profile.panels[j].q for j in range(profile.len)]) + profile.gamma * sum(
        [At[i][j] for j in range(profile.len)]) + V * np.sin(a)

    return vtx, vty

vx, vy = vxvy(1,0,profile)
print(vx,vy)