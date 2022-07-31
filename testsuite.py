from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from scenario.errorcylindertheoretical import errorcylindertheoretical
from scenario.eightsidedcylindererror import eightsidedcylindererror
from scenario.eightsidedcylinderpanelparameters import eightsidedcylinderpanelparameters
from scenario.makeprofilegraphs import makeprofilegraphs
from scenario.writecylinderintocircle import writecylinderintocircle
from scenario.novortexsystemmatrix import novortexsystemmatrix
from scenario.analyticalcylinder import analyticalcylinder
from scenario.cylinderqvc import cylinderqvc
from scenario.rotatingcylinder import rotatingcylinder
"""
got = []
theo = []
nas = []
error = []
for n in range(75,200):
    x, y, R, muy = make_joukowski( N=n)
    panels = make_panels(x, y)
    profile = AirfoilProfile(panels)

    profile.solve(a=5)
    got.append(profile.ca)
    th = joukowski_ca(5,R,muy, profile.t)
    theo.append(th)
    #print(profile.ca)
    #print(th)
    nas.append(n)
    error.append(abs(th - profile.ca))
n = len(got)
meaner = 1/n * sum(error)
meanth = 1/n * sum(theo)
relerror = meaner/meanth * 100
print(relerror)
"""
"""
fig, ax1 = plt.subplots(1, constrained_layout=True)
ax1.plot(nas, theo, color='k', linestyle=':', linewidth=1, label='$c_a^\mathrm{theoretich}$')
ax1.plot(nas, got, color='k', linestyle='-', linewidth=1, label="$c_a^\mathrm{exakt}$")

ax1.grid(True)
ax1.legend(prop={'size': 10})


plt.show()

"""

#8-seitiger Zylinder zwischen -15 und 15 grad
#rotatingcylinder()

#q, vt, cp für 8-seitigen Zylinder
#cylinderqvc()

#Analytische Lösung 8-seitgier Zylinder
#analyticalcylinder()

#Systemmatrix 8-seitiger Zylinder
#novortexsystemmatrix()

#Zylinder in Kreis einschreiben
#writecylinderintocircle()

#BigGraphs
#besser: über scenario-Folder starten
#makeprofilegraphs()

# Panelparameter 8-seitig
#eightsidedcylinderpanelparameters()

# Grafik Abweichung Berechnung Theorie
#eightsidedcylindererror()

# error kreiszylinder theoretischer wert
#errorcylindertheoretical()
