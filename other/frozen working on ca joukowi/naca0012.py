from helper import make_continuuous_loop, parsecoords, make_panels
from profile import AirfoilProfile
import numpy as np
from panel import Panel
from math import atan2

filename = "NACA0012.DAT"
make_continuuous_loop(filename)

x, y = parsecoords("data/processeddata/" + filename)
#print((atan2(y[len(x)-2] - y[len(x)-1],x[len(x)-2] - x[len(x)-1])+2*numpy.pi)*180/numpy.pi)

#x = numpy.flipud(x)
#y = numpy.flipud(y)
panels = make_panels(x, y)
print([(panel.xa, panel.ya, panel.xb, panel.yb) for panel in panels])
profile = AirfoilProfile(panels, filename)

#profile.write_panels()
#for a in range(0,40,1):
 #   a = a/2
  #  a = np.radians(a)
profile.solve()
   # print(a*180/np.pi, profile.ca)


#cps = profile.compute_theoretical_cp()
#cps2 = [panel.cp for panel in panels]

#print(cps)
#print(cps2)
profile.plot()