from helper import make_panels, parsecoords, define_panels
from profile_new import AirfoilProfile
from make_cylinder import cylinder, circle
from joukowski import make_joukowski, make_karman_trefftz, joukowski_ca
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit
import os

def plot(profile, height=8, width=5, sort=False, normalvectors=False, scaled=False):
    fig, (ax1, ax2, ax3) = plt.subplots(3, constrained_layout=True)
    fig.set_figheight(height)
    fig.set_figwidth(width)
    # fig.suptitle(f'{profile.name}')

    profilelower = [panel for panel in profile.panels if panel.loc == "lower"]
    profileupper = [panel for panel in profile.panels if panel.loc == "upper"]

    xu = [panel.xb for panel in profileupper]
    xu.append(profileupper[-1].xa)
    xl = [panel.xb for panel in profilelower]
    xl.append(profilelower[-1].xa)
    yu = [panel.yb for panel in profileupper]
    yu.append(profileupper[-1].ya)
    yl = [panel.yb for panel in profilelower]
    yl.append(profilelower[-1].ya)

    if sort:
        coordsu = [(x, y) for x, y in zip(xu, yu)]
        coordsu.sort(reverse=True)
        xu = [c[0] for c in coordsu]
        yu = [c[1] for c in coordsu]
        coordsl = [(x, y) for x, y in zip(xl, yl)]
        coordsl.sort()
        xl = [c[0] for c in coordsl]
        yl = [c[1] for c in coordsl]

    ax1.grid()
    ax1.plot(xu, yu, color='g', linestyle='-', linewidth=1, label='Oberseite')
    ax1.plot(xl, yl, color='k', linestyle='-', linewidth=1, label='Unterseite')
    ax1.set(xlabel='$x$', ylabel='$y$')
    ax1.axis('scaled')
    ax1.set_ylim([-0.2, 0.2])
    ax1.set_title("Profilform")

    if normalvectors:
        X = np.zeros(2)  # Initialize panel X variable
        Y = np.zeros(2)  # Initialize panel Y variable
        count = 0
        for panel in profile.panels:  # Loop over all panels
            X[0] = panel.xm  # Panel starting X point
            X[1] = panel.xm + panel.length * np.cos(panel.delta)  # Panel ending X point
            Y[0] = panel.ym  # Panel starting Y point
            Y[1] = panel.ym + panel.length * np.sin(panel.delta)  # Panel ending Y point
            if (count == 0):  # For first panel
                ax1.plot(X, Y, 'b-', label='First Panel')  # Plot the first panel normal vector
            elif (count == 1):  # For second panel
                ax1.plot(X, Y, 'g-', label='Second Panel')  # Plot the second panel normal vector
            else:  # For every other panel
                ax1.plot(X, Y, 'k')
            count += 1
    ax1.legend(loc='upper right', prop={'size': 8})

    # theta = [panel.theta * 180 / np.pi for panel in profile.panels]
    thetau = [panel.theta for panel in profileupper]
    thetal = [panel.theta for panel in profilelower]
    theta = []
    for go in [thetau, thetal]:
        for i in range(len(go)):
            if 3*np.pi/2 < go[i] <= 2* np.pi:
                # print(go[i])
                go[i] -= 2 * np.pi
                # print(go[i])
                go[i] = go[i] * 180 / np.pi
                # print(go[i])
            else:
                go[i] = go[i] * 180 / np.pi

    theta.append(max(thetal))
    theta.append(max(thetau))
    theta.append((min(thetal)))
    theta.append((min(thetau)))
    xml = [panel.xm for panel in profile.panels if panel.loc == "lower"]
    xmu = [panel.xm for panel in profile.panels if panel.loc == "upper"]
    xmu.reverse()
    #xl.reverse()
    #yl.reverse()
    # thetal.pop(0)
    # thetal.pop(-1)
    thetau.reverse()
    #xl.reverse()
    # thetal.append(thetau[0])
    ax2.plot(xmu[1:], thetau[1:], color='g', linestyle=':', linewidth=2, label='Oberseite')
    ax2.plot(xml, thetal, color='k', linestyle=':', linewidth=2, label='Unterseite')
    ax2.set(xlabel='$x$', ylabel='$\\theta$ $[\mathrm{grad}]$')
    ax2.set_title("Neigungswinkel")
    ax2.set_yticks(np.linspace(min(theta), max(theta), 7))
    #ax2.set_yticks([min(theta)] + [(min((theta)) + 270) / 2] + [270] + [(max((theta)) + 270) / 2] + [max(theta)])
    #ax2.set_yticks([min(theta)]+ [45] + [90] + [135]  + [max(theta)])
    ax2.legend(loc='best', prop={'size': 8})

    lu = [panel.length for panel in profileupper]
    ll = [panel.length for panel in profilelower]

    ll.reverse()
    # lu.append(ll[0])
    ax3.plot(xmu, lu, color='g', linestyle=':', linewidth=2, label='Oberseite')
    ax3.plot(xml, ll, color='k', linestyle=':', linewidth=2, label='Unterseite')
    ax3.set(xlabel='$x$', ylabel='$\ell$  $[\mathrm{m}]$')
    ax3.set_title("Panellänge")
    ax3.legend(loc='best', prop={'size': 8})

    # plt.savefig('data/figures/' + profile.name + ".png")
    plt.show()

    # plt.clf()


def makeprofileplot():
    #for filename in os.listdir("data/rawdata"):
        #print(filename)
    x, y = parsecoords("data/rawdata/nlf105.dat")
    panels = make_panels(x, y)
    profile = AirfoilProfile(panels)

    plot(profile)
