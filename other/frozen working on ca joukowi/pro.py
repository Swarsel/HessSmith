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

        self.ca = None
        self.accuracy = None
        self.gamma = None

    def solve(self, V=1, a=np.radians(4.0)):
        b = compute_inhomogenity(self.panels, self.vortex, V, a)
        qs = np.linalg.solve(self.M, b)

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

        self.ca = - 2 / (V * self.t) * sum([panel.vt * panel.length for panel in self.panels])
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
