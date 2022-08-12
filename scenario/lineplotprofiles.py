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
from scipy.optimize import curve_fit

def lineplotprofiles():
    for filename in os.listdir("data/rawdata"):

        print(filename)
        x, y = parsecoords("data/processeddata/" + filename)
        #x, y = parsecoords("data/" + filename)
        panels = make_panels(x, y)
        profile = AirfoilProfile(panels, vortex=True)

        profile.solve(V=1, a=5)
        cp1t = [panel.cp for panel in panels if panel.loc == "upper"]
        cp1b = [panel.cp for panel in panels if panel.loc == "lower"]
        vt1t = [panel.vt for panel in panels if panel.loc == "upper"]
        vt1b = [panel.vt for panel in panels if panel.loc == "lower"]

        profile.solve(V=1, a=8)
        cp2t = [panel.cp for panel in panels if panel.loc == "upper"]
        cp2b = [panel.cp for panel in panels if panel.loc == "lower"]
        vt2t = [panel.vt for panel in panels if panel.loc == "upper"]
        vt2b = [panel.vt for panel in panels if panel.loc == "lower"]


        profilelower = [panel for panel in profile.panels if panel.loc == "lower"]
        profileupper = [panel for panel in profile.panels if panel.loc == "upper"]

        xu = [panel.xb for panel in profileupper]
        xl = [panel.xb for panel in profilelower]

        fig, (ax1, ax2) = plt.subplots(2, constrained_layout=True)
        fig.suptitle("Druckbeiwerte an der Oberfläche")
        ax1.grid()
        ax1.plot(xu, cp1t, color='g', marker="D", markersize=2,  linestyle='--', linewidth=1, label='Oberseite')
        ax1.plot(xl, cp1b, color='k', marker="D", markersize=2,  linestyle='--', linewidth=1, label='Unterseite')
        ax1.set(ylabel='$c_p$')
        #ax1.axis('scaled')
        ax1.set_ylim([-4, 2])
        ax1.set_title("$\\alpha = 5^{\circ}$")
        ax1.legend(loc='lower right', prop={'size': 10})
        ax2.grid()
        ax2.plot(xu, cp2t, color='g', marker="D", markersize=2, linestyle='--', linewidth=1, label='Oberseite')
        ax2.plot(xl, cp2b, color='k', marker="D", markersize=2,  linestyle='--', linewidth=1, label='Unterseite')
        ax2.set(xlabel='$x$', ylabel='$c_p$')
        #ax2.axis('scaled')
        ax2.set_ylim([-6, 4])
        ax2.set_title("$\\alpha = 8^{\circ}$")
        ax2.legend(loc='lower right', prop={'size': 10})
        plt.show()

        fig, (ax1, ax2) = plt.subplots(2, constrained_layout=True)
        fig.suptitle("Tangentialgeschwindigkeiten an der Oberfläche")
        ax1.grid()
        ax1.plot(xu, vt1t, color='g', marker="D", markersize=2, linestyle='--', linewidth=1, label='Oberseite')
        ax1.plot(xl, vt1b, color='k', marker="D", markersize=2, linestyle='--', linewidth=1, label='Unterseite')
        ax1.set(ylabel='$v^{(t)}$')
        # ax1.axis('scaled')
        ax1.set_ylim([-2, 2])
        ax1.set_title("$\\alpha = 5^{\circ}$")
        ax1.legend(loc='best', prop={'size': 10})
        ax2.grid()
        ax2.plot(xu, vt2t, color='g', marker="D", markersize=2, linestyle='--', linewidth=1, label='Oberseite')
        ax2.plot(xl, vt2b, color='k', marker="D", markersize=2, linestyle='--', linewidth=1, label='Unterseite')
        ax2.set(xlabel='$x$', ylabel='$v^{(t)}$')
        # ax2.axis('scaled')
        ax2.set_ylim([-2, 3])
        ax2.set_title("$\\alpha = 8^{\circ}$")
        ax2.legend(loc='best', prop={'size': 10})
        plt.show()