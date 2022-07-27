from math import atan2
import numpy as np


class Panel:

    def __init__(self, xa, ya, xb, yb):
        self.xa, self.ya = xa, ya  # panel starting-point
        self.xb, self.yb = xb, yb  # panel ending-point

        self.xm = (xa + xb) / 2 # center of panel on x axis
        self.ym = (ya + yb) / 2 # center of panel on y axis
        self.theta = atan2(yb - ya, xb - xa)    # angle of panel
        if self.theta < 0:  # if angle is negative, add 2pi to only have positive angles
            self.theta += 2* np.pi  # (only useful for plotting)
        self.delta = self.theta - np.pi/2   #normal angle of panel
        if self.delta < 0:
            self.delta += 2* np.pi
        if self.delta > 2*np.pi:
            self.delta -= 2*np.pi
        self.length = np.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)  # panel length

        # panel location (used for plotting)
        if np.pi/2 < self.theta < 3*np.pi/2:
            self.loc = 'upper'  # upper surface
        elif self.theta == np.pi/2 or self.theta == 3*np.pi/2:
            self.loc = 'vertical'
        else:
            self.loc = 'lower'  # lower surface

        self.q = None  # source strength
        self.vt = None  # tangential velocity
        self.cp = None  # pressure coefficient