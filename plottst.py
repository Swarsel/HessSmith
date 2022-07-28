from helper import make_continuuous_loop, parsecoords, make_panels
from profile import AirfoilProfile
import numpy as np
import matplotlib.pyplot as plt

filename = "NACA0012.DAT"
make_continuuous_loop(filename)

x, y = parsecoords("data/processeddata/" + filename)

panels = make_panels(x, y)
profile = AirfoilProfile(panels, filename)
height=5
width=5

profile.solve()
fig, ax1 = plt.subplots(1, constrained_layout=True)
fig.set_figheight(height)
fig.set_figwidth(width)
fig.suptitle(f'Kutta-Bedingung')

lower = [panel for panel in panels if panel.loc == "lower"]
upper = [panel for panel in panels if panel.loc == "upper"]

xu = [panel.xb for panel in upper]
#xu.append(upper[-1].xa)
xl = [panel.xb for panel in lower]
#xl.append(lower[-1].xa)
yu = [panel.yb for panel in upper]
#yu.append(upper[-1].ya)
yl = [panel.yb for panel in lower]
#yl.append(lower[-1].ya)

ax1.grid()
ax1.plot(xu, yu, color='r', linestyle='-', linewidth=1, label='upper')
ax1.plot(xl, yl, color='b', linestyle='-', linewidth=1, label='lower')
ax1.set(xlabel='x', ylabel='y')
ax1.set_title("Profile")

X = np.zeros(2)  # Initialize panel X variable
Y = np.zeros(2)  # Initialize panel Y variable
count = 0
for panel in panels:  # Loop over all panels
    X[0] = panel.xm  # Panel starting X point
    X[1] = panel.xm + panel.length * np.cos(panel.delta)# Panel ending X point
    Y[0] = panel.ym  # Panel starting Y point
    Y[1] = panel.ym + panel.length * np.sin(panel.delta) # Panel ending Y point
    if (count == 0):  # For first panel
        ax1.plot(X, Y, 'b-', label='First Panel')  # Plot the first panel normal vector
    elif (count == 1):  # For second panel
        ax1.plot(X, Y, 'g-', label='Second Panel')  # Plot the second panel normal vector
    count += 1
ax1.legend(loc='best', prop={'size': 8})
plt.show()