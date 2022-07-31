from helper import make_continuuous_loop, parsecoords, make_panels
from profile import AirfoilProfile
import numpy as np
import matplotlib.pyplot as plt
from joukowski import make_joukowski_all, make_joukowski, joukowski_ca, karman_trefftz, make_karman_trefftz, make_karman_trefftz_all



#x2, y2, xc, yc, tx, ty, delta, lamda = make_karman_trefftz_all(mux=0.3, muy=0.4)
#x, y = make_karman_trefftz()
#x, y = make_joukowski(lamda=0.3, delta=0.4)
#print((atan2(y[len(x)-2] - y[len(x)-1],x[len(x)-2] - x[len(x)-1])+2*numpy.pi)*180/numpy.pi)
#print(x1)

#x = numpy.flipud(x)
#y = numpy.flipud(y)
theo = []
got = []
ns = []
for n in range(10,120):
    ns.append(n)
    x1, y1, xc, yc, tx, ty, delta, lamda, Rci, R = make_joukowski_all(lamda=0.08, delta=0.08, N=n)
    panels = make_panels(x1, y1)
    profile = AirfoilProfile(panels, "joukowski")
    #print([(a,b) for a,b in zip(x1, y1)])
#profile.write_panels()
    #print(R)

    profile.solve(a=np.radians(4))
    #print(profile)
    got.append(profile.ca)
    theo.append(joukowski_ca(np.radians(4),Rci, delta, profile.t))
    #print(profile.t)

print(got)
print(theo)
#cps = profile.compute_theoretical_cp()
#cps2 = [panel.cp for panel in panels]

#print(cps)
#print(cps2)
#profile.plot(sort=True)

fig, ax1 = plt.subplots(1, constrained_layout=True)

#ax1.plot(x1, y1, color='k', linestyle='-', linewidth=1, label='Joukowski-T.')
#ax1.plot(x2, y2, color='k', linestyle='-', linewidth=1, label='Karman-Trefftz-T.')
#ax1.plot(x2, y2, color='k', linestyle='-', linewidth=1, label='Karman-Trefftz-T.')
ax1.plot(ns, got, color='g', linestyle='-', linewidth=1, label="got")
ax1.plot(ns, theo, color='k', linestyle='-', linewidth=1, label="theo")
#ax1.scatter(tx, ty, color='g', linestyle='-', linewidth=1)
#ax1.plot([0, -lamda], [0,0], color='g', linestyle='-', linewidth=2, label='$\\mu_x$')
#ax1.plot([-lamda, -lamda], [0,delta], color='g', linestyle=':', linewidth=2, label='$\\mu_y$')

fig.set_figheight(6)
fig.set_figwidth(6)
#plt.axis('scaled')
#ax1.grid(True)
#ax1.spines['left'].set_position('zero')
#ax1.spines['right'].set_color('none')
#ax1.spines['bottom'].set_position('zero')
#ax1.spines['top'].set_color('none')
#ax1.set_xticks([-2] + [-1]+[1] + [2])
#ax1.set_yticks([-1]+[1])
ax1.legend(prop={'size': 9})


plt.show()
