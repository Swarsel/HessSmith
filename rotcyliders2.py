from make_cylinder import cylinder, circle
from helper import make_panels, write_coords
from profile import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot

err = []
for npanels in range(8,9):
    #print(npanels)
    x, y = cylinder(n=npanels)

    panels = make_panels(x, y)
    profile = AirfoilProfile(panels, f"{npanels}-Sided Cylinder", vortex=False)
    for a in range(-25,25):
        profile.solve(a=np.radians(0))
    R=1
    errors = []
    for panel in panels:
        e = abs(panel.cp-(1 - 4* (panel.ym/R)**2))
        if abs(e) < 30:
            errors.append([npanels, panel.cp, 1 - 4* (panel.ym/R)**2, 100*abs(panel.cp-(1 - 4* (panel.ym/R)**2))/(1 - 4* (panel.ym/R)**2),e])

    sum = 0
    for error in errors:
        sum += error[4]
    #print(errors)
    sum /= len(error)
    print(sum)
    err.append(sum)
n= range(5,101)
y = [1/(np.e**i) for i in n]
pyplot.figure(figsize=(5, 5))
pyplot.grid()
pyplot.xlabel("$n$ Panels", fontsize=16)
pyplot.ylabel('$e_{c_p}$', fontsize=16)
pyplot.scatter(err, color='k')
#pyplot.plot(n, y, color='g', linestyle=':', linewidth=1)

pyplot.show()
