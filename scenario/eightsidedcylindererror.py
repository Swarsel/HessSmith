from make_cylinder import cylinder, circle
from helper import make_panels
from profile_new import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot

def eightsidedcylindererror():

    x, y, _ = cylinder(n=8)
    panels = make_panels(x, y)

    profile = AirfoilProfile(panels, vortex=False)
    profile.solve(a=np.radians(0))

    x_c, y_c, R = circle(N=100)

    #cc_analytical = 2 * (1-4*(y_c / R) ** 2) +1
    cp_analytical = 1.0 - 4 * (y_c / R) ** 2
    #cps2 = [panel.cp for panel in panels]
    #print([(panel.xm, panel.cp) for panel in panels])
    """
    """
    pyplot.figure(figsize=(5, 5))
    pyplot.grid()
    pyplot.xlabel("$x$", fontsize=16)
    pyplot.ylabel('$c_p$', fontsize=16)
    pyplot.plot(x_c, cp_analytical, label="$2 \cos{(2 \\varphi)} -1$", color='k', linestyle=':', linewidth=1)
    pyplot.scatter([p.xm for p in panels], [p.cp for p in panels],
                   label='8-seitiger Zylinder', marker="^",
                   color='g', s=20, zorder=2)

    #pyplot.title('Number of panels : %d' % 10, fontsize=16)
    print([(p.theta+np.pi/2, p.cp) for p in panels])
    pyplot.legend(loc='lower right', prop={'size': 10})
    #pyplot.axis('scaled')
    #pyplot.xlim(-1.0, 1.0)
    pyplot.ylim(-4.0, 2.0)
    pyplot.show()