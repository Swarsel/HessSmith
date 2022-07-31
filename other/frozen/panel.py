from math import atan2
import numpy as np
import math

class Panel:

    def __init__(self, xa, ya, xb, yb):
        self.xa, self.ya = xa, ya  # panel starting-point
        self.xb, self.yb = xb, yb  # panel ending-point

        self.xm = (xa + xb) / 2  # center of panel on x axis
        self.ym = (ya + yb) / 2  # center of panel on y axis
        self.length = np.sqrt((xb - xa) ** 2 + (yb - ya) ** 2)  # panel length

        self.theta = atan2(yb - ya, xb - xa)  # angle of panel
        if self.theta < 0:  # if angle is negative, add 2pi to only have positive angles
            self.theta += 2 * np.pi  # (only useful for plotting)

        # normal angle of panel
        self.delta = self.theta - np.pi / 2
        if self.delta < 0:
            self.delta += 2 * np.pi
        if self.delta > 2 * np.pi:
            self.delta -= 2 * np.pi
        '''
        # orientation of the panel (angle between x-axis and panel's normal)
        if xb - xa <= 0.0:
            self.beta = math.acos((yb - ya) / self.length)
        elif xb - xa > 0.0:
            self.beta = math.pi + math.acos(-(yb - ya) / self.length)

        # location of the panel
        if self.beta <= math.pi:
            self.loc = 'upper'
        else:
            self.loc = 'lower'
        '''
        # panel location (used for plotting)
        if np.pi / 2 < self.theta < 3 * np.pi / 2:
            self.loc = 'upper'  # upper surface
        elif self.theta == np.pi / 2 or self.theta == 3 * np.pi / 2:
            self.loc = 'vertical'
        else:
            self.loc = 'lower'  # lower surface
        '''
        '''
        self.q = None  # source strength
        self.vt = None  # tangential velocity
        self.cp = None  # pressure coefficient
