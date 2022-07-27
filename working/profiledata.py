import os
from helper import parsecoords, make_continuuous_loop, make_panels
import matplotlib.pyplot as plt
from profile import AirfoilProfile
import numpy as np

for filename in os.listdir("data/rawdata"):

    # get coordinates in selig format
    make_continuuous_loop(filename)

    # get x and y coordinates
    x, y = parsecoords("data/processeddata/" + filename)
    panels = make_panels(x, y)
    profile = AirfoilProfile(panels, filename[:-4])

    # write calculated values to file
    profile.write_panels()


    # make plots
    profile.plot()
    profile.solve()
    print(profile)
