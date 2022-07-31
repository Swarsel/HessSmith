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

def definitionpanel():
    fig, ax1 = plt.subplots(1, constrained_layout=True)

    plt.plot([0, 4], [0, 0], color="k", linewidth=1, linestyle="--")
    plt.arrow(0, 0, 4, 2, head_width=0.01, color="k", fc="k", linewidth=0.5)
    AngleAnnotation((0, 0), (4, 0), (4, 2), ax=ax1, size=700, text="$\\theta_i$", textposition="inside",
                    text_kw=dict(fontsize=14, xytext=(1, 0)))
    plt.scatter(0, 0, marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_i$", (0, 0.17), fontsize=14)
    plt.scatter(4, 2, marker="D", color='k', fc="None", linewidth=0.5)
    plt.annotate("$\\vec x_{i+1}$", (3.5, 2.1), fontsize=14)
    plt.scatter(2, 1, marker="+", color='k', s=100, linewidth=0.5)
    plt.annotate("$\\vec X_{i}$", (2, 1.3), fontsize=14)
    plt.arrow(0, 0, 1.5, 0.75, head_width=0.1, color="k", fc="k", linewidth=0.5)
    plt.annotate("$s$", (0.7, 0.5), fontsize=14)

    fig.set_figheight(4)
    fig.set_figwidth(4)
    plt.axis('scaled')
    # ax1.grid(True)
    ax1.spines['left'].set_color('none')
    ax1.spines['right'].set_color('none')
    ax1.spines['bottom'].set_color('none')
    ax1.spines['top'].set_color('none')
    ax1.set_xticks([])
    ax1.set_yticks([])

    plt.savefig('data/scenarios/FIGURES/panel.png')
    plt.show()