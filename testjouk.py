from helper import make_continuuous_loop, parsecoords, make_panels
from profile import AirfoilProfile
import numpy as np
import matplotlib.pyplot as plt
from joukowski import make_joukowski_all, karman_trefftz, make_karman_trefftz

#x, y, xc, yc, tx, ty, delta, lamda = make_joukowski_all()
x, y = make_karman_trefftz()
#print((atan2(y[len(x)-2] - y[len(x)-1],x[len(x)-2] - x[len(x)-1])+2*numpy.pi)*180/numpy.pi)

#x = numpy.flipud(x)
#y = numpy.flipud(y)
panels = make_panels(x, y)
profile = AirfoilProfile(panels, "joukowski")

#profile.write_panels()

profile.solve()
print(profile.ca)


#cps = profile.compute_theoretical_cp()
#cps2 = [panel.cp for panel in panels]

#print(cps)
#print(cps2)
#profile.plot(sort=True)

fig, ax1 = plt.subplots(1, constrained_layout=True)
ax1.plot(x, y, color='b', linestyle='-', linewidth=1, label='Joukowski-Transform')
#ax1.plot(xc, yc, color='r', linestyle='-', linewidth=1, label='Complex Circle')
#ax1.scatter(tx, ty, color='g', linestyle='-', linewidth=1, label='Center')
#ax1.plot([0, -lamda], [0,0], color='g', linestyle='-', linewidth=2, label='$\lambda$')
#ax1.plot([-lamda, -lamda], [0,delta], color='g', linestyle='-', linewidth=2, label='$\delta$')

fig.set_figheight(6)
fig.set_figwidth(6)
plt.axis('scaled')
#ax1.grid(True)
ax1.spines['left'].set_position('zero')
ax1.spines['right'].set_color('none')
ax1.spines['bottom'].set_position('zero')
ax1.spines['top'].set_color('none')
ax1.set_xticks([-2] + [-1]+[1] + [2])
ax1.set_yticks([-1]+[1])
ax1.legend()


plt.show()