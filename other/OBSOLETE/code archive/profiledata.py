import os
from helper import parsecoords, split_xy, make_continuuous_loop
from computations import compute_vals, compute_circumference
import matplotlib.pyplot as plt

for filename in os.listdir("data/rawdata"):

    # get coordinates in selig format
    make_continuuous_loop(filename)

    # get x and y coordinates
    coords = parsecoords("data/processeddata/" + filename)
    x, y = split_xy(coords)
    n = len(x)

    # compute circumference of profile
    U = compute_circumference(x, y)

    # compute profile data
    X, Y, theta, l = compute_vals(x, y)

    # write calculated values to file
    with open("data/vals/" + filename[:-4] + "_vals.dat", "w+") as file:
        file.write(f"Circumference: {U} \n")
        file.write(f"X_i, Y_i, theta_i, l_i\n")
        for i in range(len(X)):
            file.write(f"{X[i]}, {Y[i]}, {theta[i]}, {l[i]}\n")


    # close loops for plotting
    if (x[0], y[0]) != (x[-1], y[-1]):
        x.append(x[0])
        y.append(y[0])
    # make plots

    fig, (ax1, ax2, ax3) = plt.subplots(3, constrained_layout=True)
    fig.suptitle(f'{filename}')
    ax1.grid()
    ax1.plot(x, y, color='k', linestyle='-', linewidth=1)
    ax1.set(xlabel='x', ylabel='y')
    ax1.set_title("Profile")

    ax2.plot(theta, color='k', linestyle='-', linewidth=1)
    ax2.set(xlabel='n', ylabel='theta [rad]')
    ax2.set_title("Angle of Panel")

    ax3.plot(l, color='k', linestyle='-', linewidth=1)
    ax3.set(xlabel='n', ylabel='l [m]')
    ax3.set_title("Panel length")

    plt.show()
