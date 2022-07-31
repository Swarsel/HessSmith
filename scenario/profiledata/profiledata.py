import os
from helper import parsecoords, make_panels
import matplotlib.pyplot as plt
from profile import AirfoilProfile
import numpy as np

for filename in os.listdir("data/"):
    print(filename)
    x, y = parsecoords("data/" + filename)
    panels = make_panels(x, y)
    profile = AirfoilProfile(panels, name="")

    profile.plot()


