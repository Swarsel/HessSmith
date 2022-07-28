from make_cylinder import cylinder, circle
from helper import make_panels, write_coords
from profile import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot

for npanels in range(8, 9):
    for a in range(0, 1):
        x, y = cylinder(n=100)
        panels = make_panels(x, y)
        profile = AirfoilProfile(panels, f"{npanels}-Sided Cylinder", vortex=False)

        profile.solve(a=np.radians(0))
        #print(profile)
        #profile.plot()

    x_c, y_c = circle(N=100)
    R=1

    cp_analytical = 1.0 - 4 * (y_c / R)**2
    cps2 = [panel.cp for panel in panels]
    print([(panel.xm, panel.cp) for panel in panels])

    pyplot.figure(figsize=(10, 6))
    pyplot.grid()
    pyplot.xlabel('x', fontsize=16)
    pyplot.ylabel('$C_p$', fontsize=16)
    pyplot.plot(x_c, cp_analytical,
                label='analytical',
                color='b', linestyle='-', linewidth=1, zorder=1)
    pyplot.scatter([p.xm for p in panels], [p.cp for p in panels],
                   label='source-panel method',
                   color='#CD2305', s=40, zorder=2)
    pyplot.title('Number of panels : %d' % 10, fontsize=16)
    pyplot.legend(loc='best', prop={'size': 16})
    pyplot.xlim(-1.0, 1.0)
    pyplot.ylim(-4.0, 2.0)
    pyplot.show()