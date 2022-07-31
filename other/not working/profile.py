from computations import compute_xi, compute_eta, compute_J, compute_I, compute_At, compute_An, system_matrix, \
    compute_inhomogenity, compute_An_free, compute_At_free, compute_eta_free, compute_xi_free, compute_I_free, compute_J_free
import matplotlib.pyplot as plt
import numpy as np
import csv

class AirfoilProfile:
    def __init__(self, panels, name, vortex=True):
        self.panels = panels
        self.name = name
        self.len = len(self.panels)
        self.vortex = vortex

        self.U = sum([panel.length for panel in self.panels])
        self.xi = compute_xi(self.len, self.panels)
        self.eta = compute_eta(self.len, self.panels)
        self.I = compute_I(self.len, self.xi, self.eta, self.panels)
        self.J = compute_J(self.len, self.xi, self.eta, self.panels)
        self.An = compute_An(self.len, self.I, self.J, self.panels)
        self.At = compute_At(self.len, self.I, self.J, self.panels)
        self.M = system_matrix(self.An, self.At, self.vortex)

        self.x = [panel.xa for panel in self.panels]
        self.y = [panel.ya for panel in self.panels]
        self.t = abs(max(self.x) - min(self.x))
        self.coords = [(panel.xa, panel.ya, panel.xb, panel.yb) for panel in self.panels]
        self.lower = [panel for panel in self.panels if panel.loc == "lower"]
        self.upper = [panel for panel in self.panels if panel.loc == "upper"]

        if max([panel.ya for panel in self.lower]) > max([panel.ya for panel in self.upper]):
            self.lower, self.upper = self.upper, self.lower
        self.ca = None
        self.accuracy = None
        self.gamma = None

    def __str__(self):
        return f"Theta:\n" \
               f"{[panel.theta * 180 / np.pi for panel in self.panels]}\n" \
               f"Delta:\n" \
               f"{[panel.delta * 180 / np.pi for panel in self.panels]}\n" \
               f"An:\n" \
               f"{self.An}\n" \
               f"At:\n" \
               f"{self.At}\n" \
               f"M:\n" \
               f"{self.M}\n" \
               f"Source:\n" \
               f"{[panel.q for panel in self.panels]}\n" \
               f"vt:\n" \
               f"{[panel.vt for panel in self.panels]}\n" \
               f"Pressure coefficients:\n" \
               f"{[panel.cp for panel in self.panels]}\n" \
               f"Accuracy:\n" \
               f"{self.accuracy}\n" \
               f"gamma:\n" \
               f"{self.gamma}\n" \
               f"Lift coefficient:\n" \
               f"{self.ca}"

    def solve(self, V=1, a=np.radians(4.0)):
        b = compute_inhomogenity(self.panels, self.vortex, V, a)
        qs = np.linalg.solve(self.M, b)
        #print(b)
        for i, panel in enumerate(self.panels):
            panel.q = qs[i]
        if self.vortex:
            self.gamma = qs[-1]

        if self.vortex:
            vt = []
            for i in range(self.len):
                vt.append(
                    sum([self.At[i][j] * self.panels[j].q for j in range(self.len)]) - self.gamma * sum(
                        [self.An[i][j] for j in range(self.len)]) + V * np.cos(
                        a - self.panels[i].theta))
        else:
            vt = []
            for i in range(self.len):
                vt.append(
                    sum([self.At[i][j] * self.panels[j].q for j in range(self.len)]) + V * np.cos(
                        a - self.panels[i].theta))
        for i, panel in enumerate(self.panels):
            panel.vt = vt[i]

        for panel in self.panels:
            panel.cp = 1 - (panel.vt / V) ** 2

        self.ca = -2 / (V * self.t) * sum([panel.vt * panel.length for panel in self.panels])
        self.accuracy = sum([panel.q * panel.length for panel in self.panels])

    def write_panels(self):
        header = ["X_i", "Y_i", "theta_i", "l_i"]
        with open("data/vals/" + self.name + "_vals.csv", "w+", encoding='UTF8',newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            #file.write(f"Circumference: {self.U} \n")
            #file.write(f"X_i, Y_i, theta_i, l_i\n")
            for panel in self.panels:
                #file.write(f"{panel.xm}, {panel.ym}, {panel.theta}, {panel.length}\n")
                writer.writerow([panel.xm, panel.ym, panel.theta, panel.length])
    def plot(self, height=3, width=6, sort=False, normalvectors=False, scaled=False):
        fig, (ax1) = plt.subplots(1, constrained_layout=True)
        fig.set_figheight(height)
        fig.set_figwidth(width)
        #fig.suptitle(f'{self.name}')

        xu = [panel.xb for panel in self.upper]
        xu.append(self.upper[-1].xa)
        xl = [panel.xb for panel in self.lower]
        xl.append(self.lower[-1].xa)
        yu = [panel.yb for panel in self.upper]
        yu.append(self.upper[-1].ya)
        yl = [panel.yb for panel in self.lower]
        yl.append(self.lower[-1].ya)

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
        ax1.plot(xu, yu, color='g', linestyle='-', linewidth=1, label='upper')
        ax1.plot(xl, yl, color='k', linestyle='-', linewidth=1, label='lower')
        ax1.set(xlabel='x', ylabel='y')
        ax1.axis('scaled')
        #ax1.set_ylim([-0.2, 0.2])
        #ax1.set_title("Profile")
        """
        if normalvectors:
            X = np.zeros(2)  # Initialize panel X variable
            Y = np.zeros(2)  # Initialize panel Y variable
            count = 0
            for panel in self.panels:  # Loop over all panels
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

        #theta = [panel.theta * 180 / np.pi for panel in self.panels]
        thetau = [panel.theta for panel in self.upper]
        thetal = [panel.theta for panel in self.lower]
        theta = []
        for go in [thetau, thetal]:
            for i in range(len(go)):
                if go[i] <= np.pi/2:
                    #print(go[i])
                    go[i]+= 2* np.pi
                    #print(go[i])
                    go[i] = go[i] * 180/np.pi
                    #print(go[i])
                else:
                    go[i] = go[i] * 180 / np.pi

        theta.append(max(thetal))
        theta.append(max(thetau))
        theta.append((min(thetal)))
        theta.append((min(thetau)))

        xl.reverse()
        yl.reverse()
        # thetal.pop(0)
        #thetal.pop(-1)
        thetau.reverse()
        # thetal.append(thetau[0])
        ax2.plot(thetau, color='g', linestyle=':',  linewidth=2, label='upper')
        ax2.plot(thetal, color='k', linestyle=':', linewidth=2, label='lower')
        ax2.set(xlabel='x', ylabel='theta [grad]')
        ax2.set_title("Angle of Panel")
        #ax2.set_yticks(np.arange(min(theta), max(theta) + 1, 40.0))
        ax2.set_yticks([min(theta)] + [(min((theta)) + 270)/2] + [270] + [(max((theta)) + 270)/2] + [max(theta)])
        ax2.legend(loc='best', prop={'size': 8})

        lu = [panel.length for panel in self.upper]
        ll = [panel.length for panel in self.lower]

        ll.reverse()
        # lu.append(ll[0])
        ax3.plot(lu, color='g', linestyle=':',  linewidth=2, label='upper')
        ax3.plot(ll, color='k', linestyle=':', linewidth=2, label='lower')
        ax3.set(xlabel='x', ylabel='l [m]')
        ax3.set_title("Panel length")
        ax3.legend(loc='best', prop={'size': 8})

        #if scaled:
        """
        plt.savefig('data/figures/' + self.name + ".png")
        plt.show()

        #plt.clf()

    def compute_free_vt(self, x, y, V=1, a=np.radians(4.0)):
        eta = compute_eta_free(len(x), self.len, self.panels, x, y)
        xi = compute_xi_free(len(x), self.len, self.panels, x, y)
        I = compute_I_free(len(x), self.len, xi, eta, self.panels)
        J = compute_J_free(len(x), self.len, xi, eta, self.panels)
        An = compute_An_free(len(x), self.len, I, J, self.panels)
        At = compute_At_free(len(x), self.len, I, J, self.panels)

        vtx = np.empty(len(x))
        vty = np.empty(len(x))
        for i in range(len(x)):
            vtx[i] = sum([At[i][j] * self.panels[j].q for j in range(self.len)]) - self.gamma * sum(
                [An[i][j] for j in range(self.len)]) + V * np.cos(a)

            vty[i] = sum([An[i][j] * self.panels[j].q for j in range(self.len)]) + self.gamma * sum(
                [At[i][j] for j in range(self.len)]) + V * np.sin(a)

        return vtx, vty
