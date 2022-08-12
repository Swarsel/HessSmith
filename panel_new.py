import numpy as np

def ensure_zero(scalar):
    if abs(scalar) < 10 ** (-15):
        scalar = 0
    return scalar

class Panel:

    def __init__(self, xa, ya, xb, yb, index):
        self.index = index
        self.xa, self.ya = xa, ya
        self.xb, self.yb = xb, yb

        self.xm = (xa + xb) / 2
        self.ym = (ya + yb) / 2
        self.length = ensure_zero(np.sqrt((xb - xa) ** 2 + (yb - ya) ** 2))
        self.theta = np.arctan2(yb - ya, xb - xa)
        # für einfachere Interpretation beim Plotten

        if self.theta < 0:
            self.theta += 2*np.pi

        if np.pi / 2 < self.theta < 3 * np.pi / 2:
            self.loc = 'lower'  # upper surface
        elif self.theta == np.pi / 2 or self.theta == 3 * np.pi / 2:
            self.loc = 'vertical'
        else:
            self.loc = 'upper'  # lower surface

        self.q = None
        self.vt = None
        self.cp = None

    def __str__(self):
        return f"Panel {self.index}: {(self.xa, self.ya)} -> {(self.xb, self.yb)}; " \
               f"X_{self.index}: {self.xm}; " \
               f"Y_{self.index}: {self.ym}; " \
               f"Winkel θ_{self.index}: {self.theta * 180 / np.pi}°; " \
               f"Länge l_{self.index}: {self.length}"
