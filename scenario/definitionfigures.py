import matplotlib

from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
from external.AngleAnnotation import AngleAnnotation
import matplotlib.patches as patches

def definitionfigures():
    x,y = parsecoords("data/processeddata/naca0012b.dat")
    y *= 1.3
    fig, ax1 = plt.subplots(1, constrained_layout=True)

    ax1.plot(x, y, color='k', linestyle=':', linewidth=1)
    ax1.scatter(x[0], y[0], marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_0 = \\vec x_n$", (x[0], y[0]+0.018), fontsize=14)
    ax1.scatter(x[10], y[10], marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_1 $", (x[10], y[10]+0.02), fontsize=14)
    ax1.scatter(x[15], y[15], marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_2 $", (x[15], y[15]+0.02), fontsize=14)
    ax1.scatter(x[-10], y[-10], marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_{n-1} $", (x[-10], y[-10]-0.04), fontsize=14)
    ax1.scatter(x[-15], y[-15], marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_{n-2} $", (x[-15]-0.03, y[-15]-0.043), fontsize=14)
    ax1.scatter(x[60], y[60], marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_{i+1} $", (x[60]-0.06, y[60]+0.02), fontsize=14)
    ax1.scatter(x[55], y[55], marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_{i} $", (x[55], y[55]+0.02), fontsize=14)
    plt.arrow(0,-0.35, 0, 0.2,head_width=0.01, color="k", fc="k",linewidth=0.5)
    plt.annotate("$y$", (0.02, -0.15), fontsize=14)
    plt.arrow(0,-0.35, 0.2, 0,head_width=0.01, color="k", fc="k",linewidth=0.3)
    plt.annotate("$x$", (0.2, -0.33), fontsize=14)
    plt.plot([0.1,0.28], [-0.25,-0.25], color="k", linewidth=1, linestyle = "--")
    plt.annotate("$\\vec V_{\infty}$", (0.2, -0.17), fontsize=14)
    plt.arrow(0.1,-0.25, 0.15, 0.07,head_width=0.01, color="k", fc="k",linewidth=0.5)
    AngleAnnotation((0.1,-0.25), (0.28, -0.25), (0.25, -0.18), ax=ax1, size=190, text="$\\alpha$", textposition = "inside", text_kw=dict(fontsize=14, xytext = (1,0)))
    #plt.arrow(0.8,-0.1, -0.2, -0.07,head_width=0.01, color="k", fc="k", arrowprops = dict(arrowstyle="->", connectionstyle="arc3,rad=-0.2"))

    style = "Simple, tail_width=0.5, head_width=4, head_length=8"
    kw = dict(arrowstyle=style, color="k")
    a3 = patches.FancyArrowPatch((1, -0.1),(0.7, -0.15),
                                 connectionstyle="arc3,rad=-.1", **kw)
    plt.gca().add_patch(a3)
    plt.annotate("Zählrichtung Panele $\mathcal{C}_i$", (0.8, -0.2), fontsize=16)

    a3 = patches.FancyArrowPatch((1, 0.1),(0.7, 0.15),
                                 connectionstyle="arc3,rad=.1", **kw)
    plt.gca().add_patch(a3)
    plt.annotate("Zählrichtung \nKoordinatenpaare $\\vec x_i$", (0.48, 0.1), fontsize=16)

    for k in range(4,11):
        ax1.scatter(x[5*k], y[5*k], marker="D", color='k', fc="None", linewidth=0.5)
    for k in range(13, 23):
        ax1.scatter(x[5 * k], y[5 * k], marker="D", color='k', fc="None", linewidth=0.5)

    fig.set_figheight(4)
    fig.set_figwidth(9)
    plt.axis('scaled')
    # ax1.grid(True)
    ax1.spines['left'].set_color('none')
    ax1.spines['right'].set_color('none')
    ax1.spines['bottom'].set_color('none')
    ax1.spines['top'].set_color('none')
    ax1.set_xticks([])
    ax1.set_yticks([])

    plt.savefig('data/scenarios/FIGURES/zaehlrichtung.png')
    plt.show()

