from computations import compute_xi, compute_eta, compute_J, compute_I, compute_At, compute_An, system_matrix, \
    compute_inhomogenity
import sympy as sym
import matplotlib.pyplot as plt
import numpy as np


class AirfoilProfile:
    def __init__(self, panels, name, vortex=True):
        self.panels = panels
        self.name = name
        self.len = len(self.panels)
        self.vortex = vortex

        self.U = sum([panel.length for panel in selfpanels])
        self.xi = compute_xi(self.len, self.panels)
        self.eta = compute_eta(self.len, selfpanels)
        self.I = compute_I(self.len, self.xi, self.eta, self.panels)
        self.J = compute_J(self.len, self.xi, self.eta, self.panels)
        self.An = compute_An(self.len, self.I, self.J, self.panels)
        self.At = compute_At(self.len, self.I, self.J, self.panels)
        self.M = system_matrix(self.An, self.At, self.vortex)

        self.x = [panel.xa for panel in self.panels]
        self.y = [panel.ya for panel in self.panels]
        self.lower = [panel for panel in self.panels if panel.loc == "lower"]
        self.upper = [panel for panel in self.panels if panel.loc == "upper"]

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

    def solve(self, V=1, a=np.radians(4.0), t=1):
        b = compute_inhomogenity(self.panels, self.vortex, V, a)
        qs = np.linalg.solve(self.M, b)
        print(b)
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
                    sum([self.At[i][j] * self.panels[j].q for j in range(self.len)]) + V * sym.cos(
                        a - self.panels[i].theta))
        for i, panel in enumerate(self.panels):
            panel.vt = vt[i]

        for panel in self.panels:
            panel.cp = 1 - (panel.vt / V) ** 2

        self.ca = - 2 / (V * t) * sum([panel.vt * panel.length for panel in self.panels])
        self.accuracy = sum([panel.q * panel.length for panel in self.panels])

    def write_panels(self):
        with open("data/vals/" + self.name + "_vals.dat", "w+") as file:
            file.write(f"Circumference: {self.U} \n")
            file.write(f"X_i, Y_i, theta_i, l_i\n")
            for panel in self.panels:
                file.write(f"{panel.xm}, {panel.ym}, {panel.theta}, {panel.length}\n")

    def plot(self, height=8, width=5):
        fig, (ax1, ax2, ax3) = plt.subplots(3, constrained_layout=True)
        fig.set_figheight(height)
        fig.set_figwidth(width)
        fig.suptitle(f'{self.name}')

        xu = [panel.xb for panel in self.upper]
        xu.append(self.upper[-1].xa)
        xl = [panel.xb for panel in self.lower]
        xl.append(self.lower[-1].xa)
        yu = [panel.yb for panel in self.upper]
        yu.append(self.upper[-1].ya)
        yl = [panel.yb for panel in self.lower]
        yl.append(self.lower[-1].ya)

        ax1.grid()
        ax1.plot(xu, yu, color='r', linestyle='-', linewidth=1, label='upper')
        ax1.plot(xl, yl, color='b', linestyle='-', linewidth=1, label='lower')
        ax1.set(xlabel='x', ylabel='y')
        ax1.set_title("Profile")

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
        ax1.legend(loc='best', prop={'size': 8})

        theta = [panel.theta * 180 / np.pi for panel in self.panels]
        thetau = [panel.theta * 180 / np.pi for panel in self.upper]
        thetal = [panel.theta * 180 / np.pi for panel in self.lower]
        # thetal.pop(0)
        thetal.pop(-1)
        # thetal.append(thetau[0])
        ax2.plot(thetau, color='r', linestyle=':', marker=".", linewidth=1, label='upper')
        ax2.plot(thetal, color='b', linestyle=':', marker=".", linewidth=1, label='lower')
        ax2.set(xlabel='n', ylabel='theta [grad]')
        ax2.set_title("Angle of Panel")
        ax2.set_yticks(np.arange(min(theta), max(theta) + 1, 40.0))
        ax2.legend(loc='best', prop={'size': 8})

        lu = [panel.length for panel in self.upper]
        ll = [panel.length for panel in self.lower]
        ll.pop(-1)
        # lu.append(ll[0])
        ax3.plot(lu, color='r', linestyle=':', marker=".", linewidth=1, label='upper')
        ax3.plot(ll, color='b', linestyle=':', marker=".", linewidth=1, label='lower')
        ax3.set(xlabel='n', ylabel='l [m]')
        ax3.set_title("Panel length")
        ax3.legend(loc='best', prop={'size': 8})
        plt.show()
