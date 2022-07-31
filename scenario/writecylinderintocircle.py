from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def writecylinderintocircle():
    x, y, _ = cylinder(cx=0, n=8)
    xc, yc, _ = circle(cx=0, N=1000)

    fig, ax1 = plt.subplots(1, constrained_layout=True)
    ax1.plot(x, y, color='g', linestyle='-', linewidth=1)
    ax1.plot(xc, yc, color='k', linestyle='-', linewidth=1)

    fig.set_figheight(3)
    fig.set_figwidth(3)
    plt.axis('scaled')
    # ax1.grid(True)
    ax1.spines['left'].set_position('zero')
    ax1.spines['right'].set_color('none')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['top'].set_color('none')
    ax1.set_xticks([])
    ax1.set_yticks([])

    plt.show()
