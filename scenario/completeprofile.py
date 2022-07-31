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

def completeprofile():
    #for filename in os.listdir("data/rawdata"):
    for filename in os.listdir("data/"):
        print(filename)
        #x, y = parsecoords("data/processeddata/" + filename)
        x, y = parsecoords("data/" + filename)
        panels = make_panels(x, y)
        profile = AirfoilProfile(panels, vortex=True)
        aas = []
        cas = []
        #with open("data/scenarios/completeprofile/" + filename + ".txt", "w+") as write:
        with open(filename + ".txt", "w+") as write:
            for a in range(-11, 18, 4):
                profile.solve(V=1, a=a)
                txt = str(a) + " & " + str(round(profile.gamma, 2)) + " & " + str(round(profile.ca, 2)) + " \\\\ \n"
                write.write(txt)
                aas.append(a)
                cas.append(profile.ca)

        fig, (ax1) = plt.subplots(1, constrained_layout=True)
        ax1.grid()
        fig.set_figheight(3)
        fig.set_figwidth(3)
        ax1.set(xlabel="$\\alpha$ $[grad]$", ylabel='$c_a$')
        ax1.plot(aas, cas, 'k', markersize=1)
        ax1.set_ylim([min(cas) - 0.3, max(cas) + 0.3])
        ax1.set_yticks(np.arange(min(cas), max(cas), 0.3))
        ax1.set_xticks(aas)
        plt.show()

        profile.solve(V=1, a=5)
        vx, vy = profile.compute_free_vt(x, y)

        q = [p.q for p in panels]
        cp = [p.cp for p in panels]


        plt.figure(figsize=(5, 3), layout='constrained')
        plt.title(f'$x$-Komponente von $\\vec v$')
        plt.scatter(x, y, c=vx, s=3)
        plt.axis('scaled')
        plt.xlabel("$x$", fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        plt.ylim(-0.2, 0.2)
        plt.colorbar(orientation="horizontal")
        plt.show()

        plt.figure(figsize=(5, 3), layout='constrained')
        plt.title(f'$y$-Komponente von $\\vec v$')
        plt.scatter(x, y, c=vy, s=3)
        plt.axis('scaled')
        plt.xlabel("$x$", fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        plt.ylim(-0.2, 0.2)
        plt.colorbar(orientation="horizontal")
        plt.show()

        x = [p.xm for p in panels]
        y = [p.ym for p in panels]

        plt.figure(figsize=(5, 3), layout='constrained')
        plt.title(f'Quellbelegung')
        plt.scatter(x, y, c=q, s=3)
        plt.axis('scaled')
        plt.xlabel("$x$", fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        plt.ylim(-0.2, 0.2)
        plt.colorbar(orientation="horizontal")
        plt.show()

        plt.figure(figsize=(5, 3), layout='constrained')
        plt.title(f'Druckbeiwerte')
        plt.scatter(x, y, c=cp, s=3)
        plt.axis('scaled')
        plt.xlabel("$x$", fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        plt.ylim(-0.2, 0.2)
        plt.colorbar(orientation="horizontal")
        plt.show()


completeprofile()