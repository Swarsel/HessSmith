import numpy as np

def ensure_zero(scalar):
    if abs(scalar) < 10 ** (-15):
        scalar = 0
    return scalar

class Panel:

    def __init__(self, xa, ya, xb, yb, index, flip=False):
        self.index = index
        self.xa, self.ya = xa, ya
        self.xb, self.yb = xb, yb

        self.xm = (xa + xb) / 2
        self.ym = (ya + yb) / 2
        self.length = ensure_zero(np.sqrt((xb - xa) ** 2 + (yb - ya) ** 2))
        if not flip:
            self.theta = np.arctan2(yb - ya, xb - xa)
        if flip:
            self.theta = np.arctan2(ya - yb, xa - xb)
        if self.theta < 0:
            self.theta += 2 * np.pi  # für einfachere Interpretation

        self.q = None
        self.vt = None
        self.cp = None

    def __str__(self):
        return f"Panel {self.index}: {(self.xa, self.ya)} -> {(self.xb, self.yb)}; " \
               f"Xm: {self.xm}; " \
               f"Ym: {self.ym}; " \
               f"Angle: {self.theta * 180 / np.pi}; " \
               f"Length: {self.length}"
