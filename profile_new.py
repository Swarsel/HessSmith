import comp
import numpy as np
import csv
import free

class AirfoilProfile:
    def __init__(self, panels, name=None, vortex=True):
        self.panels = panels
        self.name = name
        self.x = [panel.xa for panel in self.panels]
        self.y = [panel.ya for panel in self.panels]
        self.len = len(self.panels)
        self.vortex = vortex

        self.U = sum([panel.length for panel in self.panels])
        self.t = abs(max(self.x) - min(self.x))

        self.xi = comp.xi(self)
        self.eta = comp.eta(self)
        self.I = comp.I(self)
        self.J = comp.J(self)
        self.An = comp.An(self)
        self.At = comp.At(self)
        self.M = comp.M(self)

        self.ca = None
        self.accuracy = None
        self.gamma = None

    def __str__(self):
        return f"An:\n" \
               f"{self.An}\n" \
               f"At:\n" \
               f"{self.At}\n" \
               f"M:\n" \
               f"{self.M}\n" \
               f"q:\n" \
               f"{[panel.q for panel in self.panels]}\n" \
               f"vt:\n" \
               f"{[panel.vt for panel in self.panels]}\n" \
               f"cp:\n" \
               f"{[panel.cp for panel in self.panels]}\n" \
               f"acc: {self.accuracy}\n" \
               f"gamma: {self.gamma}\n" \
               f"ca: {self.ca}"

    def write_panels(self, filename, n=2):
        header = ["X_i", "Y_i", "theta_i", "l_i"]
        with open(filename, "w+", encoding='UTF8',newline="") as file:
            writer = csv.writer(file)
            writer.writerow(header)
            for panel in self.panels:
                writer.writerow([round(panel.xm,n), round(panel.ym,n), round(panel.theta*180/np.pi,n), round(panel.length,n)])

    def solve(self, V=1, a=5):
        a = np.radians(a)
        b = comp.b(self, V, a)

        comp.q(self, b)  # setzt auch self.gamma
        comp.vt(self, V, a)
        comp.cp(self, V)
        comp.ca(self, V)
        comp.accuracy(self)

    def compute_free_vt(self, x, y, V=1, a=np.radians(4.0)):
        #x = x[:-1]
        #y = y[:-1]
        eta = free.compute_eta_free(len(x), self.len, self.panels, x, y)
        xi = free.compute_xi_free(len(x), self.len, self.panels, x, y)
        I = free.compute_I_free(len(x), self.len, xi, eta, self.panels)
        J = free.compute_J_free(len(x), self.len, xi, eta, self.panels)
        An = free.compute_An_free(len(x), self.len, I, J, self.panels)
        At = free.compute_At_free(len(x), self.len, I, J, self.panels)

        vtx = np.empty(len(x))
        vty = np.empty(len(x))
        for i in range(len(x)):
            vtx[i] = sum([At[i][j] * self.panels[j].q for j in range(self.len)]) - self.gamma * sum(
                [An[i][j] for j in range(self.len)]) + V * np.cos(a)

            vty[i] = sum([An[i][j] * self.panels[j].q for j in range(self.len)]) + self.gamma * sum(
                [At[i][j] for j in range(self.len)]) + V * np.sin(a)

        return vtx, vty
