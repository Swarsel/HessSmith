from make_cylinder import cylinder, circle
from helper import make_panels, parsecoords
from profile_new import AirfoilProfile
from joukowski import make_joukowski
import numpy as np
import matplotlib.pyplot as plt
import sympy as sym
from sympy import Number
from sympy.solvers.solveset import linsolve
import os

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

def custom():
    for filename in os.listdir("data/rawdata"):
    #for filename in os.listdir("data/"):
        print(filename)
        x, y = parsecoords("data/processeddata/" + filename)
        #x, y = parsecoords("data/" + filename)
        panels = make_panels(x, y)
        profile = AirfoilProfile(panels, vortex=True)

        nx, ny = 100, 100  # number of points in the x and y directions
        x_start, x_end = -0.5, 1.5
        y_start, y_end = -0.2, 0.2
        X, Y = np.meshgrid(np.linspace(x_start, x_end, nx),
                           np.linspace(y_start, y_end, ny))

        xs = X[0]
        ys = np.array([yi[0] for yi in Y])

        a=5
        V=1
        vx, vy = get_velocity_field(profile, xs, ys, X.shape, Y.shape, V=V, a=a)

        mat = np.matrix(vx)
        with open('data/scenarios/completeprofile/' + filename[:-4] + 'vx100.txt', 'w+') as f:
            for line in mat:
                np.savetxt(f, line, fmt='%.8f')
        mat = np.matrix(vy)
        with open('data/scenarios/completeprofile/' + filename[:-4] + 'vy100.txt', 'w+') as f:
            for line in mat:
                np.savetxt(f, line, fmt='%.8f')

        plt.figure(figsize=(5, 3), layout='constrained')
        plt.xlabel('$x$', fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        plt.streamplot(X, Y, vx, vy,
                       density=1, linewidth=0.5, arrowsize=1, arrowstyle='->')
        plt.fill(profile.x,
                 profile.y,
                 color='k', linestyle='solid', linewidth=2, zorder=2)
        plt.axis('scaled')
        plt.xlim(x_start, x_end)
        plt.ylim(y_start, y_end)
        plt.title(f'Umströmung',fontsize=16)
        #plt.savefig('data/scenarios/FIGURES/' + filename[:-4] + 'stream.png')
        plt.show()