import numpy as np
import csv

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

        self.xi = self.__xi()
        self.eta = self.__eta()
        self.I = self.__i()
        self.J = self.__j()
        self.An = self.__an()
        self.At = self.__at()
        self.M = self.__m()

        self.ca = None
        self.accuracy = None
        self.gamma = None

    def __str__(self):
        return f"xi:\n" \
               f"{self.xi}\n" \
               f"eta:\n" \
               f"{self.eta}\n" \
               f"I:\n" \
               f"{self.I}\n" \
               f"J:\n" \
               f"{self.J}\n" \
               f"An:\n" \
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

    def __xi(self, x=None, y=None):
        panels = self.panels
        n_panels = len(panels)
        if x and y:
            n = len(x)
        else:
            n = len(panels)
        Xi = np.zeros((n, n_panels), dtype=float)
        for i in range(n):
            for j in range(n_panels):
                if x and y:
                    i_xm, i_ym = x[i], y[i]
                else:
                    i_xm, i_ym = panels[i].xm, panels[i].ym
                pj = panels[j]
                Xi[i][j] = (i_xm - pj.xm) * np.cos(pj.theta) + (i_ym - pj.ym) * np.sin(pj.theta)
                #Xi[i][j] = ensure_zero(Xi[i][j])
        return Xi

    def __eta(self, x=None, y=None):
        panels = self.panels
        n_panels = len(panels)
        if x and y:
            n = len(x)
        else:
            n = len(panels)
        Eta = np.zeros((n, n_panels), dtype=float)
        for i in range(n):
            for j in range(n_panels):
                if x and y:
                    i_xm, i_ym = x[i], y[i]
                else:
                    i_xm, i_ym = panels[i].xm, panels[i].ym
                pj = panels[j]
                Eta[i][j] = - (i_xm - pj.xm) * np.sin(pj.theta) + (i_ym - pj.ym) * np.cos(pj.theta)
                #Eta[i][j] = ensure_zero(Eta[i][j])
        return Eta

    def __i(self, Xi=None, Eta=None):
        panels = self.panels
        if not Xi and not Eta:
            Xi = self.xi
            Eta = self.eta
        n_panels = len(panels)
        n = Xi.shape[0]
        II = np.zeros((n, n_panels), dtype=float)
        for i in range(n):
            for j in range(n_panels):
                pj = panels[j]
                if i == j and n > 1:
                    II[i][j] = 0
                else:
                    II[i][j] = (1 / (4 * np.pi)) * np.log(((pj.length + 2 * Xi[i][j]) ** 2 + 4 * (Eta[i][j] ** 2)) /
                                                          ((pj.length - 2 * Xi[i][j]) ** 2 + 4 * (Eta[i][j] ** 2)))
                #II[i][j] = ensure_zero(II[i][j])
        return II

    def __j(self, Xi=None, Eta=None):
        panels = self.panels
        if not Xi and not Eta:
            Xi = self.xi
            Eta = self.eta
        n_panels = len(panels)
        n = Xi.shape[0]
        JJ = np.zeros((n, n_panels), dtype=float)
        for i in range(n):
            for j in range(n):
                pj = panels[j]
                if i == j and n > 1:
                    JJ[i][j] = 0.5
                else:
                    JJ[i][j] = (1 / (2 * np.pi)) * np.arctan2(pj.length - 2 * Xi[i][j], 2 * Eta[i][j]) + \
                               (1 / (2 * np.pi)) * np.arctan2(pj.length + 2 * Xi[i][j], 2 * Eta[i][j])
                #JJ[i][j] = ensure_zero(JJ[i][j])
        return JJ

    def __an(self, II=None, JJ=None):
        panels = self.panels
        if not II and not JJ:
            II = self.I
            JJ = self.J
        n_panels = len(panels)
        n = II.shape[0]
        if n == 1:
            i_theta = 0
        AN = np.zeros((n, n_panels), dtype=float)
        for i in range(n):
            for j in range(n_panels):
                if n > 1:
                    i_theta = panels[i].theta
                pj = panels[j]
                # if i == j:
                AN[i][j] = - np.sin(i_theta - pj.theta) * II[i][j] + np.cos(i_theta - pj.theta) * JJ[i][j]
                # else:
                #   AN[i][j] = + np.sin(pi.theta - pj.theta) * II[i][j] - np.cos(pi.theta - pj.theta) * JJ[i][j]
                #AN[i][j] = ensure_zero(AN[i][j])
        return AN

    def __at(self, II=None, JJ=None):
        panels = self.panels
        if not II and not JJ:
            II = self.I
            JJ = self.J
        n_panels = len(panels)
        n = II.shape[0]
        if n == 1:
            i_theta = 0
        AT = np.zeros((n, n_panels), dtype=float)
        for i in range(n):
            for j in range(n):
                if n > 1:
                    i_theta = panels[i].theta
                pj = panels[j]
                AT[i][j] = np.cos(i_theta - pj.theta) * II[i][j] + np.sin(i_theta - pj.theta) * JJ[i][j]
                #AT[i][j] = ensure_zero(AT[i][j])
        return AT

    def __m(self):
        panels = self.panels
        AN = self.An
        AT = self.At
        vortex = self.vortex
        n = len(panels)
        if vortex:
            MM = np.zeros((n + 1, n + 1), dtype=float)
        else:
            MM = np.zeros((n, n), dtype=float)
        if vortex:
            MM[:-1, :-1] = AN
            MM[:-1, -1] = np.sum(AT, axis=1)

            r = np.zeros(n + 1, dtype=float)
            r[:-1] = AT[0, :] + AT[n - 1, :]
            r[-1] = -np.sum(AN[0, :] + AN[n - 1, :])
            MM[-1, :] = r
        else:
            MM = AN
        #for i in range(len(MM)):
         #   for j in range(len(MM)):
          #      MM[i][j] = ensure_zero(MM[i][j])
        return MM

    def solve(self, V=1, a=5):
        a = np.radians(a)
        b = self.__b(V, a)

        self.__q(b)  # setzt auch self.gamma
        self.__vt(V, a)
        self.__cp(V)
        self.__ca(V)
        self.__accuracy()

    def compute_free_vt(self, x, y, V=1, a=5):
        a = np.radians(a)
        #x = x[:-1]
        #y = y[:-1]
        xi = self.__xi(x=x, y=y)
        eta = self.__eta(x=x, y=y)
        I = self.__i(Xi=xi, Eta=eta)
        J = self.__j(Xi=xi, Eta=eta)
        An = self.__an(II=I, JJ=J)
        At = self.__at(II=I, JJ=J)

        vtx = np.empty(len(x))
        vty = np.empty(len(x))
        for i in range(len(x)):
            vtx[i] = sum([At[i][j] * self.panels[j].q for j in range(self.len)]) - self.gamma * sum(
                [An[i][j] for j in range(self.len)]) + V * np.cos(a)

            vty[i] = sum([An[i][j] * self.panels[j].q for j in range(self.len)]) + self.gamma * sum(
                [At[i][j] for j in range(self.len)]) + V * np.sin(a)

        return vtx, vty

    def __b(self, V, a):
        panels = self.panels
        vortex = self.vortex
        n = len(panels)
        if vortex:
            B = np.zeros(n + 1, dtype=float)
        else:
            B = np.zeros(n, dtype=float)
        for i in range(n):
            pi = panels[i]
            B[i] = -V * np.sin(a - pi.theta)
        if vortex:
            B[-1] = -V * (np.cos(a - panels[0].theta) + np.cos(a - panels[-1].theta))
        # for i in range(len(B)):
        #   B[i] = ensure_zero(B[i])
        # print(B)
        return B

    def __q(self, B):
        panels = self.panels
        qs = np.linalg.solve(self.M, B)

        for i, panel in enumerate(panels):
            panel.q = qs[i]
        if self.vortex:
            self.gamma = qs[-1]

    def __vt(self, V, a):
        panels = self.panels
        AN = self.An
        AT = self.At
        n = len(panels)
        if self.vortex:
            VT = np.zeros(n, dtype=float)
            for i in range(n):
                VT[i] = sum([AT[i][j] * panels[j].q for j in range(n)]) \
                        - self.gamma * sum([AN[i][j] for j in range(n)]) \
                        + V * np.cos(a - panels[i].theta)
        else:
            VT = np.zeros(n, dtype=float)
            for i in range(n):
                VT[i] = sum([AT[i][j] * panels[j].q for j in range(n)]) \
                        + V * np.cos(a - panels[i].theta)
        # for i in range(len(VT)):
        #   VT[i] = ensure_zero(VT[i])
        for i, panel in enumerate(panels):
            panel.vt = VT[i]

    def __cp(self, V):
        for panel in self.panels:
            panel.cp = 1 - (panel.vt / V) ** 2

    def __ca(self, V):
        self.ca = 2 / (V * self.t) * sum([panel.vt * panel.length for panel in self.panels])

    def __accuracy(self):
        self.accuracy = sum([panel.q * panel.length for panel in self.panels])

