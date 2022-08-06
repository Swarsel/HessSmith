from helper import parsecoords, make_panels
from profile_new import AirfoilProfile
import numpy as np
import matplotlib.pyplot as plt
from joukowski import make_joukowski_all, make_karman_trefftz_all


def joukowskiplots():
    x2, y2, xc, yc, tx, ty, muy, mux = make_karman_trefftz_all(mux=0.3, muy=0.4)
    x1, y1, xc, yc, tx, ty, muy, mux, Rci, R = make_joukowski_all(mux=0.3, muy=0.4)

    #cps = profile.compute_theoretical_cp()
    #cps2 = [panel.cp for panel in panels]

    #print(cps)
    #print(cps2)
    #profile.plot(sort=True)

    fig, ax1 = plt.subplots(1, constrained_layout=True)
    ax1.plot(x1, y1, color='k', linestyle='-', linewidth=1, label='Joukowski-T.')
    ax1.plot(xc, yc, color='g', linestyle='-', linewidth=1, label="$\\zeta$-Kreis")
    ax1.scatter(tx, ty, color='g', linestyle='-', linewidth=1)
    ax1.plot([0, -mux], [0,0], color='g', linestyle='-', linewidth=2, label='$\\mu_x$')
    ax1.plot([-mux, -mux], [0,muy], color='g', linestyle=':', linewidth=2, label='$\\mu_y$')
    fig.set_figheight(6)
    fig.set_figwidth(6)
    plt.axis('scaled')
    #ax1.grid(True)
    ax1.spines['left'].set_position('zero')
    ax1.spines['right'].set_color('none')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['top'].set_color('none')
    ax1.set_xticks([-2] + [-1]+[1] + [2])
    ax1.set_yticks([-1]+[1])
    ax1.legend(prop={'size': 9})
    plt.savefig('data/scenarios/FIGURES/joukowski.png')
    plt.show()


    fig, ax1 = plt.subplots(1, constrained_layout=True)
    ax1.plot(x2, y2, color='k', linestyle='-', linewidth=1, label='Kármán-Trefftz-T.')
    ax1.plot(xc, yc, color='g', linestyle='-', linewidth=1, label="$\\zeta$-Kreis")
    ax1.scatter(tx, ty, color='g', linestyle='-', linewidth=1)
    ax1.plot([0, -mux], [0,0], color='g', linestyle='-', linewidth=2, label='$\\mu_x$')
    ax1.plot([-mux, -mux], [0,muy], color='g', linestyle=':', linewidth=2, label='$\\mu_y$')
    fig.set_figheight(6)
    fig.set_figwidth(6)
    plt.axis('scaled')
    #ax1.grid(True)
    ax1.spines['left'].set_position('zero')
    ax1.spines['right'].set_color('none')
    ax1.spines['bottom'].set_position('zero')
    ax1.spines['top'].set_color('none')
    ax1.set_xticks([-2] + [-1]+[1] + [2])
    ax1.set_yticks([-1]+[1])
    ax1.legend(prop={'size': 9})
    plt.savefig('data/scenarios/FIGURES/karmantrefftz.png')
    plt.show()

