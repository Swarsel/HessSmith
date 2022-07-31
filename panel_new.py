import numpy as np


class Panel:

    def __init__(self, xa, ya, xb, yb):
        self.xa, self.ya = xa, ya
        self.xb, self.yb = xb, yb

        self.xm = (xa + xb) / 2
        self.ym = (ya + yb) / 2
        self.length = np.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)
        self.theta = np.arctan2(yb - ya, xb - xa)
        if self.theta < 0:
            self.theta += 2 * np.pi  # für einfachere Interpretation

        self.q = None
        self.vt = None
        self.cp = None

    def __str__(self):
        return f"{(self.xa, self.ya)} -> {(self.xb, self.yb)}; " \
               f"Angle: {self.theta * 180 / np.pi}; " \
               f"Length: {self.length}"
