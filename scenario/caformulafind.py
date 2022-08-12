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

def caformulafind():
    for filename in os.listdir("data/rawdata"):

        print(filename)
        x, y = parsecoords("data/processeddata/" + filename)
        #x, y = parsecoords("data/" + filename)
        panels = make_panels(x, y)
        profile = AirfoilProfile(panels, vortex=True)
        aas = []
        cas = []
        with open("data/scenarios/completeprofile/" + filename + ".txt", "w+") as write:
        #with open(filename + ".txt", "w+") as write:
            for a in range(-15, 16, 1):
                profile.solve(V=1, a=a)
                txt = str(a) + " & " + str(round(profile.gamma, 2)) + " & " + str(round(profile.ca, 2)) + " \\\\ \n"
                write.write(txt)
                aas.append(a)
                cas.append(profile.ca)

        def objective(x, a, b):
            return a * x + b

        xaas = np.asarray(aas)
        ycas = np.asarray(cas)
        popt, _ = curve_fit(objective, xaas, ycas)
        # summarize the parameter values
        a, b = popt
        print('e = %.5f * x + %.5f' % (a, b))
        x_line = np.arange(min(aas), max(aas), 1)
        y_line = objective(x_line, a, b)
        plt.figure(figsize=(5, 5))
        plt.grid()
        plt.xlabel("Anstellwinkel $\\alpha \; [grad]$", fontsize=16)
        plt.ylabel('$c_a$', fontsize=16)
        plt.plot(aas, cas, color='k', label="$c_a^{\mathrm{berechnet}}$")
        plt.plot(x_line, y_line, color='g', linestyle=':', label='$%.2f \\alpha + %.2f$' % (a, b))
        plt.legend()
        # plt.plot(n, y, color='g', linestyle=':', linewidth=1)
        #plt.savefig('data/scenarios/FIGURES/eightsidedcylindererror.png')
        plt.show()

        alphanull = -b/a
        print(f"alphanull (wo ca null wird): {alphanull}")
        canull = b
        print(f"caanull (ca bei alpha null): {canull}")
        """
        fig, (ax1) = plt.subplots(1, constrained_layout=True)
        ax1.grid()
        fig.set_figheight(3)
        fig.set_figwidth(3)
        ax1.set(xlabel="$\\alpha$ $[grad]$", ylabel='$c_a$')
        ax1.plot(aas, cas, 'k', markersize=1)
        ax1.set_ylim([min(cas) - 0.3, max(cas) + 0.3])
        ax1.set_yticks(np.arange(min(cas), max(cas), 0.3))
        ax1.set_xticks(aas)
        plt.savefig('data/scenarios/FIGURES/' + filename[:-4] + 'ca.png')
        plt.show()

        nx, ny = 200, 200  # number of points in the x and y directions
        x_start, x_end = -0.5, 1.5
        y_start, y_end = -0.2, 0.2
        X, Y = np.meshgrid(np.linspace(x_start, x_end, nx),
                           np.linspace(y_start, y_end, ny))

        xs = X[0]
        ys = np.array([yi[0] for yi in Y])

        a=5
        V=1
        vx, vy = get_velocity_field(profile, xs, ys, X.shape, Y.shape, V=V, a=a)

        mat = np.matrix(vx)
        with open('data/scenarios/completeprofile/' + filename[:-4] + 'vx.txt', 'w+') as f:
            for line in mat:
                np.savetxt(f, line, fmt='%.8f')
        mat = np.matrix(vy)
        with open('data/scenarios/completeprofile/' + filename[:-4] + 'vy.txt', 'w+') as f:
            for line in mat:
                np.savetxt(f, line, fmt='%.8f')

        plt.figure(figsize=(5, 3), layout='constrained')
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
        plt.savefig('data/scenarios/FIGURES/' + filename[:-4] + 'stream.png')

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
        plt.savefig('data/scenarios/FIGURES/' + filename[:-4] + 'contourcp.png')
        plt.show()


        x = [p.xm for p in panels]
        y = [p.ym for p in panels]
        q = [p.q for p in panels]
        cp = [p.cp for p in panels]

        plt.figure(figsize=(5, 3), layout='constrained')
        plt.title(f'Quellbelegung')
        plt.scatter(x, y, c=q, s=3)
        plt.axis('scaled')
        plt.xlabel("$x$", fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        plt.ylim(-0.2, 0.2)
        plt.colorbar(orientation="horizontal")
        plt.savefig('data/scenarios/FIGURES/' + filename[:-4] + 'q.png')
        plt.show()

        plt.figure(figsize=(5, 3), layout='constrained')
        plt.title(f'Druckbeiwerte an der Oberfläche des Profils')
        plt.scatter(x, y, c=cp, s=3)
        plt.axis('scaled')
        plt.xlabel("$x$", fontsize=16)
        plt.ylabel('$y$', fontsize=16)
        plt.ylim(-0.2, 0.2)
        plt.colorbar(orientation="horizontal")
        plt.savefig('data/scenarios/FIGURES/' + filename[:-4] + 'cp.png')
        plt.show()
        """