from make_cylinder import cylinder, circle
from helper import make_panels
from profile_new import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as plt

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
    plt.figure(figsize=(5, 5))
    plt.grid()
    plt.xlabel("$x$", fontsize=16)
    plt.ylabel('$c_p$', fontsize=16)
    plt.plot(x_c, cp_analytical, label="$2 \cos{(2 \\varphi)} -1$", color='k', linestyle=':', linewidth=1)
    plt.scatter([p.xm for p in panels], [p.cp for p in panels],
                   label='8-seitiger Zylinder', marker="^",
                   color='g', s=20, zorder=2)

    #plt.title('Number of panels : %d' % 10, fontsize=16)
    print([(p.theta+np.pi/2, p.cp) for p in panels])
    plt.legend(loc='lower right', prop={'size': 10})
    #plt.axis('scaled')
    #plt.xlim(-1.0, 1.0)
    plt.ylim(-4.0, 2.0)
    plt.savefig('data/scenarios/FIGURES/eightsidedcylindertheo.png')
    plt.show()
