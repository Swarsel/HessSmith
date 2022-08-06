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
from shapely.geometry import Point, Polygon
from scenario.definitionfigures import definitionfigures

#definitionfigures()

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
"""
x,y = parsecoords("data/processeddata/naca0012b.dat")


panels = make_panels(x,y)
profile = AirfoilProfile(panels, vortex=True)
#profile.solve(a=5)
#print(profile)
"""
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
def get_velocity_field(profile, XX, YY, xshape, yshape, a=0, V=1):
    #a = np.radians(a)
    # freestream contribution
    nx = xshape
    ny = yshape
    vx = np.zeros(nx, dtype=float)
    vy = np.zeros(ny, dtype=float)
    for i in range(len(XX)):
        for j in range(len(YY)):
            vx[j][i], vy[j][i] = profile.compute_free_vt(XX[i],YY[j], a=a,V=V)
            #print(XX[i], YY[j], vx[i][j], vy[i][j])

    return vx, vy

coords = [(a,b) for a,b in zip(profile.x, profile.y)]
#print(coords)
polygon = Polygon(coords)
print(polygon)

#xpp,ypp = polygon.exterior.xy
#plt.plot(xpp,ypp)
#plt.show()

# define a mesh grid
nx, ny = 80, 80  # number of points in the x and y directions
x_start, x_end = -0.5, 1.5
y_start, y_end = -0.2, 0.2
X, Y = np.meshgrid(np.linspace(x_start, x_end, nx),
                      np.linspace(y_start, y_end, ny))
xs = X[0]
ys = np.array([yi[0] for yi in Y])
vx, vy = get_velocity_field(profile, xs, ys, X.shape, Y.shape, V=1, a=5)
#print(xs)
"""
"""
for i in range(len(xs)):
    for j in range(len(ys)):
        point = Point(xs[i], ys[j])
        #print(point)
        if point.within(polygon) or polygon.touches(point):
            print(point, "is within poly")
            vx[j][i], vy[j][i] = np.nan, np.nan
"""
"""
# compute the velocity field on the mesh grid

#print(vy)
# plot the velocity field
width = 10
plt.figure(figsize=(width, width))
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)
plt.streamplot(X, Y, vx, vy,
                  density=1, linewidth=0.5, arrowsize=1, arrowstyle='->')
plt.fill(profile.x,
            profile.y,
            color='k', linestyle='solid', linewidth=2, zorder=2)
plt.axis('scaled')
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.title('Streamlines around a NACA 0012 airfoil (AoA = ${}^o$)'.format(0),
             fontsize=16)
plt.show()

# compute the pressure field
cp = 1.0 -(vx**2 + vy**2) / 1**2
# plot the pressure field
width = 10
plt.figure(figsize=(width, width))
plt.xlabel('x', fontsize=16)
plt.ylabel('y', fontsize=16)

contf = plt.contourf(X, Y, cp,
                        levels=np.linspace(-2.0, 1.0, 100), extend='both')
cbar = plt.colorbar(contf,
                       orientation='horizontal',
                       shrink=0.5, pad = 0.1,
                       ticks=[-2.0, -1.0, 0.0, 1.0])
cbar.set_label('$C_p$', fontsize=16)
plt.fill(profile.x,
            profile.y,
            color='k', linestyle='solid', linewidth=2, zorder=2)
#plt.scatter(X,Y)
plt.axis('scaled')
plt.xlim(x_start, x_end)
plt.ylim(y_start, y_end)
plt.title('Contour of pressure field', fontsize=16)
plt.show()
"""

x,y = parsecoords("data/processeddata/0213.dat")
panels = make_panels(x,y)
profile = AirfoilProfile(panels)
profile.write_panels("ok", n=8)