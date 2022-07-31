from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit

def errorcylindertheoretical():
    err = []
    nas = []
    for npanels in range(5,101):
        #print(npanels)
        x, y, R= cylinder(n=npanels)

        panels = make_panels(x, y)
        profile = AirfoilProfile(panels, vortex=False)
        for a in range(-25,25):
            profile.solve(a=0)
            #print(profile)

        errors = []
        for panel in panels:
            e = abs(panel.cp-(1 - 4* (panel.ym/R)**2))
            if abs(e) < 30:
                errors.append([npanels, panel.cp, 1 - 4* (panel.ym/R)**2, 100*abs(panel.cp-(1 - 4* (panel.ym/R)**2))/(1 - 4* (panel.ym/R)**2),e])

        sum = 0
        for error in errors:
            sum += error[4]
        #print(errors)
        sum /= len(errors)
        #print(sum)
        err.append(sum)
        nas.append(npanels)

    def objective(x, a, b):
        return (a/x**2) + b
    xn = np.asarray(nas)
    yerr = np.asarray(err)
    popt, _ = curve_fit(objective, xn, yerr)
    # summarize the parameter values
    a, b = popt
    print('e = %.5f / n + %.5f' % (a, b))
    x_line = np.arange(min(nas), max(nas), 1)
    y_line = objective(x_line, a, b)
    plt.figure(figsize=(5, 5))
    plt.grid()
    plt.xlabel("Panelanzahl $n$", fontsize=16)
    plt.ylabel('$e_{c_p}$', fontsize=16)
    plt.plot(nas,err, color='k', label="$\Delta c_{p_i}$")
    plt.plot(x_line,y_line, color='g', linestyle=':', label="17.85/n^2")
    plt.legend()
    #plt.plot(n, y, color='g', linestyle=':', linewidth=1)

    plt.show()