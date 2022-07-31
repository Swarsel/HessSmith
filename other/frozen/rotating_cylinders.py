from make_cylinder import cylinder, circle
from helper import make_panels, write_coords
from profile import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as pyplot

for npanels in range(8, 9):
    for a in range(0, 1):
        x4, y4 = cylinder(n=6)
        x8, y8 = cylinder(n=8)
        x16, y16 = cylinder(n=16)
        panels4 = make_panels(x4, y4)
        panels8 = make_panels(x8, y8)
        panels16 = make_panels(x16, y16)
        profile4 = AirfoilProfile(panels4, f"4-Sided Cylinder", vortex=False)
        profile8 = AirfoilProfile(panels8, f"4-Sided Cylinder", vortex=True)
        profile16 = AirfoilProfile(panels16, f"4-Sided Cylinder", vortex=False)

        profile4.solve(a=np.radians(0))
        profile8.solve(a=np.radians(0))
        profile16.solve(a=np.radians(0))
        # print(profile)
        # profile.plot()
    """
    xc, yc = circle(N=1000)
    fig, ax1 = pyplot.subplots(1, constrained_layout=True)
    ax1.plot(x, y, color='b', linestyle='-', linewidth=1, label='Jou')
    ax1.plot(xc, yc, color='b', linestyle='-', linewidth=1, label='Joukowski-Transform')
    # ax1.plot(xc, yc, color='r', linestyle='-', linewidth=1, label='Complex Circle')
    # ax1.scatter(tx, ty, color='g', linestyle='-', linewidth=1, label='Center')
    # ax1.plot([0, -lamda], [0,0], color='g', linestyle='-', linewidth=2, label='$\lambda$')
    # ax1.plot([-lamda, -lamda], [0,delta], color='g', linestyle='-', linewidth=2, label='$\delta$')

    fig.set_figheight(6)
    fig.set_figwidth(6)
    pyplot.axis('scaled')
    # ax1.grid(True)
    ax1.spines['left'].set_position('zero')
    ax1.spines['right'].set_color('none')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['top'].set_color('none')
    ax1.set_xticks([-2] + [-1] + [1] + [2])
    ax1.set_yticks([-1] + [1])
    ax1.legend()

    pyplot.show()
    """
    x_c, y_c = circle(N=100)
    R = 1

    #cc_analytical = 2 * (1-4*(y_c / R) ** 2) +1
    cp_analytical = 1.0 - 4 * (y_c / R) ** 2
    #cps2 = [panel.cp for panel in panels]
    #print([(panel.xm, panel.cp) for panel in panels])

    pyplot.figure(figsize=(5, 5))
    pyplot.grid()
    pyplot.xlabel("$x$", fontsize=16)
    pyplot.ylabel('$c_p$', fontsize=16)
    pyplot.plot(x_c, cp_analytical, label="$2 \cos{(2 \\varphi)} -1$", color='k', linestyle=':', linewidth=1)
    #pyplot.scatter([p.xm for p in panels4], [p.cp for p in panels4],
                   #label='6-seitiger Zylinder',
                   #color='b', s=20, zorder=2)
    pyplot.scatter([p.xm for p in panels8], [p.cp for p in panels8],
                   label='8-seitiger Zylinder', marker="^",
                   color='g', s=20, zorder=2)
    #pyplot.scatter([p.xm for p in panels16], [p.cp for p in panels16],
                   #label='10-seitiger Zylinder',
                   #color='g', s=20, zorder=2)
    #pyplot.title('Number of panels : %d' % 10, fontsize=16)
    print([(p.theta+np.pi/2, p.cp) for p in panels8])
    pyplot.legend(loc='lower right', prop={'size': 10})
    #pyplot.axis('scaled')
    #pyplot.xlim(-1.0, 1.0)
    pyplot.ylim(-4.0, 2.0)
    pyplot.show()
    vx, vy = profile8.compute_free_vt(x8, y8
                                      )
    print(vx, vy)