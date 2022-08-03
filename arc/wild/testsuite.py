import matplotlib
import free
from helper import make_panels, parsecoords, define_panels, ensure_zero
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
import math
from scipy.optimize import curve_fit
#from external.AngleAnnotation import AngleAnnotation
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

x,y = parsecoords("naca0012b.dat")


panels = make_panels(x,y)
profile = AirfoilProfile(panels, vortex=True)
profile.solve(a=5)
print(profile)
"""
def vxvy(x,y, profile,V=1, a=0):
    a=np.radians(a)
    eta = free.compute_eta_free(profile.len, profile.panels, x, y)
    #print(eta)
    xi = free.compute_xi_free(profile.len, profile.panels, x, y)
    #print(xi)
    I = free.compute_I_free(profile.len, xi, eta, profile.panels)
    #print(I)
    J = free.compute_J_free(profile.len, xi, eta, profile.panels)
    #print(J)
    An = free.compute_An_free(profile.len, I, J, profile.panels)
    #print(An)
    At = free.compute_At_free(profile.len, I, J, profile.panels)
    #print(At)
    vtx = sum([At[j] * profile.panels[j].q for j in range(profile.len)]) - profile.gamma * sum(
        [An[j] for j in range(profile.len)]) + V * np.cos(a)

    vty = sum([An[j] * profile.panels[j].q for j in range(profile.len)]) + profile.gamma * sum(
        [At[j] for j in range(profile.len)]) + V * np.sin(a)

    return vtx, vty
"""
"""
xs = []
ys = []
vxs = []
vys = []
for a,b in zip(x[1:-1],y[1:-1]):
    vx, vy = vxvy(a,b,profile, a=0)
    xs.append(a)
    ys.append(b)

    vxs.append(vx)
    vys.append(vy)
"""
"""
print([(xs[i],ys[i],vxs[i]) for i in range(len(vxs))])
print([(xs[i],ys[i],vys[i]) for i in range(len(vys))])


plt.figure(figsize=(5, 3), layout='constrained')
plt.title(f'$x$-Komponente von $\\vec v$')
plt.scatter(xs, ys, c=vxs, s=3)
plt.axis('scaled')
plt.xlabel("$x$", fontsize=16)
plt.ylabel('$y$', fontsize=16)
plt.ylim(-0.2, 0.2)
plt.colorbar(orientation="horizontal")
#plt.savefig('data/scenarios/FIGURES' + filename[:-4] + 'vx.png')
plt.show()


plt.figure(figsize=(5, 3), layout='constrained')
plt.title(f'$y$-Komponente von $\\vec v$')
plt.scatter(xs, ys, c=vys, s=3)
plt.axis('scaled')
plt.xlabel("$x$", fontsize=16)
plt.ylabel('$y$', fontsize=16)
plt.ylim(-0.2, 0.2)
plt.colorbar(orientation="horizontal")
#plt.savefig('data/scenarios/FIGURES' + filename[:-4] + 'vy.png')
plt.show()
"""

"""
def get_velocity_field(profile, X, Y, a=0, V=1):
    a = np.radians(a)
    # freestream contribution
    n = len(X)
    vx = np.zeros((n, n), dtype=float)
    vy = np.zeros((n, n), dtype=float)
    for i in range(n):
        for j in range(n):

            vx[i][j], vy[i][j] = vxvy(X[i][j],Y[i][j],profile,V=V,a=a)

    return vx, vy


# define a mesh grid
nx, ny = 20, 20  # number of points in the x and y directions
x_start, x_end = -1.0, 2.0
y_start, y_end = -0.3, 0.3
X, Y = np.meshgrid(np.linspace(x_start, x_end, nx),
                      np.linspace(y_start, y_end, ny))

# compute the velocity field on the mesh grid
vx, vy = get_velocity_field(profile, X, Y, V=1, a=0)

# plot the velocity field
width = 10
plt.figure(figsize=(width, width))
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.streamplot(X, Y, vx, vy,
                  density=1, linewidth=1, arrowsize=1, arrowstyle='->')
plt.fill([panel.xm for panel in panels],
            [panel.ym for panel in panels],
            color='k', linestyle='solid', linewidth=2, zorder=2)
plt.axis('scaled')
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.title('Streamlines around a NACA 0012 airfoil (AoA = ${}^o$)'.format(0),
             fontsize=16)
plt.show()
"""