from profile import AirfoilProfile
from make_cylinder import cylinder
from helper import make_panels, parsecoords
import numpy as np
import matplotlib.pyplot as plt

x, y = parsecoords("data/processeddata/NACA0012.DAT")
panels = make_panels(x, y)
profile = AirfoilProfile(panels, "8sided", vortex=True)

#profile.plot(scaled=True)

writer = []
cas = []
aas = []
#for a in range(-11,18, 4):
#aas.append(a)
profile.solve(a=np.radians(5.0))
vx, vy = profile.compute_free_vt(x, y)
#cas.append(profile.ca)
#writer.append(f"{a} & {round(profile.gamma,2)} & {round(profile.ca,2)} \\\\ \n")
"""
with open("data/writtendata/nlf105", "w+") as write:
    for line in writer:
        write.write(line)
"""
"""
print(cas)
fig, (ax1) = plt.subplots(1, constrained_layout=True)
ax1.grid()
fig.set_figheight(3)
fig.set_figwidth(3)
ax1.set(xlabel="$\\alpha$", ylabel='$c_a$')
ax1.plot(aas, cas, 'k', markersize=1)
ax1.set_ylim([min(cas)-0.3, max(cas)+0.3])
ax1.set_yticks(np.arange(min(cas), max(cas), 0.3))
ax1.set_xticks(aas)
plt.show()
"""
print(min(vx), max(vx))
q = [p.q for p in panels]
cp = [p.cp for p in panels]
x = [p.xm for p in panels]
y = [p.ym for p in panels]
plt.figure(figsize=(5, 3), layout='constrained')
plt.title(f'Quellbelegung')
plt.scatter(x, y, c=q, s=3)
plt.axis('scaled')
plt.xlabel("$x$", fontsize=16)
plt.ylabel('$y$', fontsize=16)
plt.ylim(-0.2,0.2)

plt.colorbar(orientation="horizontal")
plt.show()
plt.figure(figsize=(5, 3), layout='constrained')
plt.title(f'Druckbeiwerte')
plt.scatter(x, y, c=cp, s=3)
plt.axis('scaled')
plt.xlabel("$x$", fontsize=16)
plt.ylabel('$y$', fontsize=16)
plt.ylim(-0.2,0.2)

plt.colorbar(orientation="horizontal")
plt.show()