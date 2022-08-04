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



def loadandplot():
    for filename in os.listdir("data/rawdata"):
    #for filename in os.listdir("data/"):
        print(filename)
        nx, ny = 200, 200  # number of points in the x and y directions
        x_start, x_end = -0.5, 1.5
        y_start, y_end = -0.2, 0.2
        X, Y = np.meshgrid(np.linspace(x_start, x_end, nx),
                           np.linspace(y_start, y_end, ny))
        x, y = parsecoords("data/processeddata/" + filename)
        panels = make_panels(x, y)
        profile = AirfoilProfile(panels, vortex=True)

        vx = np.loadtxt('data/scenarios/completeprofile/' + filename[:-4] + "vx.txt", usecols=range(200))
        vy = np.loadtxt('data/scenarios/completeprofile/' + filename[:-4] + "vy.txt", usecols=range(200))


        plt.figure(figsize=(8, 3), layout='constrained')
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

        cp = 1.0 - (vx ** 2 + vy ** 2) / 1 ** 2
        # plot the pressure field
        plt.figure(figsize=(5, 3), layout='constrained')
        plt.xlabel('$x$', fontsize=16)
        plt.ylabel('$y$', fontsize=16)

        contf = plt.contourf(X, Y, cp,
                             levels=np.linspace(-2.0, 1.0, 100), extend='both')
        cbar = plt.colorbar(contf, orientation='horizontal',ticks=[-2.0, -1.0, 0.0, 1.0])
        cbar.set_label('$c_p$', fontsize=16)
        plt.fill(profile.x,
                 profile.y,
                 color='k', linestyle='solid', linewidth=2, zorder=2)
        # plt.scatter(X,Y)
        plt.axis('scaled')
        plt.xlim(x_start, x_end)
        plt.ylim(y_start, y_end)
        plt.title('Druckbeiwerte im Feld', fontsize=16)
        #plt.savefig('data/scenarios/FIGURES/' + filename[:-4] + 'contourcp.png')
        plt.show()
