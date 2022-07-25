import os
from numpy import sqrt
from helper import index, parsecoords, split_xy, make_continuuous_loop, compute_vals, compute_circumference
import matplotlib.pyplot as plt

for filename in os.listdir("data/rawestdata"):

    # get coordinates in closed loop form
    make_continuuous_loop(filename)
    coords = parsecoords("data/loopdata/" + filename[:-4] + "_loop.dat")

    # seperate x and y coordinates
    x, y = split_xy(coords)
    n = len(x)

    U = compute_circumference(x, y)

    X, Y, theta, l = compute_vals(x, y)

    # write calculated values to file
    with open("data/vals/" + filename[:-4] + "_vals.dat", "w+") as file:
        file.write(f"Circumference: {U} \n")
        file.write(f"X_i, Y_i, theta_i, l_i\n")
        for i in range(len(X)):
            file.write(f"{X[i]}, {Y[i]}, {theta[i]}, {l[i]}\n")

    # make plots

    fig, (ax1, ax2, ax3) = plt.subplots(3, constrained_layout=True)
    fig.suptitle(f'{filename}')
    ax1.plot(x, y)
    ax1.set(xlabel='x', ylabel='y')
    ax1.set_title("Profile")

    ax2.plot(theta[:len(theta) // 2 + 1])
    ax2.set(xlabel='n', ylabel='theta [rad]')
    ax2.set_title("Angle of Panel for half of the loop")

    ax3.plot(l[:len(theta) // 2 + 1])
    ax3.set(xlabel='n', ylabel='l [m]')
    ax3.set_title("Panel length for half of the loop")

    plt.show()
