from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def karmanerror():
    got = []
    theo = []
    nas = []
    error = []
    for n in range(10,201):
        print(n)
        x, y, R, muy = make_karman_trefftz(N=n)
        panels = make_panels(x, y)
        profile = AirfoilProfile(panels)

        profile.solve(a=5)
        got.append(profile.ca)
        th = joukowski_ca(5,R,muy, profile.t)
        theo.append(th)
        #print(profile.ca)
        #print(th)
        nas.append(n)
        error.append(abs(th - profile.ca))
    n = len(got)
    actual = 75-10-1
    meaner = 1/n * sum(error[actual:])
    meanth = 1/n * sum(theo[actual:])
    relerror = meaner/meanth * 100
    print("\n\n\n\n")
    print("Relative error:", relerror)

    fig, ax1 = plt.subplots(1, constrained_layout=True)
    ax1.plot(nas, theo, color='k', linestyle=':', linewidth=1, label='$c_a^\mathrm{theoretich}$')
    ax1.plot(nas, got, color='k', linestyle='-', linewidth=1, label="$c_a^\mathrm{exakt}$")

    ax1.grid(True)
    ax1.legend(prop={'size': 10})

    plt.savefig('data/scenarios/FIGURES/karmantrefftzerror.png')
    plt.show()
