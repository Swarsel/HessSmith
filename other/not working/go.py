import matplotlib.pyplot as plt
import numpy as np

m1, b1 = 0, 2.0 # slope & intercept (line 1)
m2, b2 = 2.0, -3.0 # slope & intercept (line 2)

#----------------------------------------------------------------------------------------#
# Step 1: plot the lines

x = np.linspace(-10,10,500)

plt.plot([2,4],[0, 2])
plt.plot(x,x*m2+b2)

plt.xlim(-2,8)
plt.ylim(-2,8)

#plt.title('How to plot an angle with matplotlib ?', fontsize=8)

#plt.savefig("plot_an_angle_matplotlib_01.png", bbox_inches='tight')

#----------------------------------------------------------------------------------------#
# Step 2: calculate the point of intersection between the two lines

x0 = (b2-b1) / (m1-m2)
y0 = m1 * x0 + b1

#plt.scatter(x0,y0, color='black' )

#plt.savefig("plot_an_angle_matplotlib_02.png", bbox_inches='tight')

#----------------------------------------------------------------------------------------#
# Step 3: plot the circle

theta = np.linspace(0, 2*np.pi, 100)

r = np.sqrt(4.0) # circle radius

x1 = r * np.cos(theta) + x0
x2 = r * np.sin(theta) + y0

#plt.plot(x1, x2, color='gray')

#plt.savefig("plot_an_angle_matplotlib_03.png", bbox_inches='tight')

#----------------------------------------------------------------------------------------#
# Step 4: calculate the points of intersection between a line and the circle

x_list = []
y_list = []

def line_and_circle_intersection_points(m,b,x0,y0,r):

    c1 = 1 + m ** 2
    c2 = - 2.0 * x0 + 2 * m * ( b - y0 )
    c3 = x0 ** 2 + ( b - y0 ) ** 2 - r ** 2

    # solve the quadratic equation:

    delta = c2 ** 2 - 4.0 * c1 * c3

    x1 = ( - c2 + np.sqrt(delta) ) / ( 2.0 * c1 )
    x2 = ( - c2 - np.sqrt(delta) ) / ( 2.0 * c1 )

    x_list.append(x1)
    x_list.append(x2)

    y1 = m * x1 + b
    y2 = m * x2 + b

    y_list.append(y1)
    y_list.append(y2)

    return None

line_and_circle_intersection_points(m1,b1,x0,y0,r)

#plt.scatter( x_list[0], y_list[0], color='black' )
#plt.scatter( x_list[1], y_list[1], color='black' )

#plt.text( x_list[0], y_list[0], 'P1', color='black' )
#plt.text( x_list[1], y_list[1], 'P2', color='black' )

line_and_circle_intersection_points(m2,b2,x0,y0,r)

#plt.scatter( x_list[2], y_list[2], color='black' )
#plt.scatter( x_list[3], y_list[3], color='black' )

#plt.text( x_list[2], y_list[2], 'P3', color='black' )
#plt.text( x_list[3], y_list[3], 'P4', color='black' )

#plt.savefig("plot_an_angle_matplotlib_04.png", bbox_inches='tight')

#----------------------------------------------------------------------------------------#
# Step 5: calculate the angle for each intersection points

def get_point_angle(x,y,x0,y0):

    num = x - x0
    den = np.sqrt( ( x - x0 )**2 + ( y - y0 )**2 )

    theta = np.arccos( num / den )

    if not y - y0 >= 0: theta = 2 * np.pi - theta

    #print(theta, np.rad2deg(theta), y - y0 )

    return theta

theta_list = []

for i in range(len(x_list)):

    x = x_list[i]
    y = y_list[i]

    theta_list.append( get_point_angle(x,y,x0,y0) )

#----------------------------------------------------------------------------------------#
# Step 6: plot the angle

theta_1 = theta_list[0]
theta_2 = theta_list[3]

theta = np.linspace(theta_1, theta_2, 100)

x1 = r * np.cos(theta) + x0
x2 = r * np.sin(theta) + y0

plt.plot(x1, x2, color='gray')

#----------------------------------------------------------------------------------------#
# Step 7: add label

mid_angle = ( theta_1 + theta_2 ) / 2.0

mid_angle_x = (r+0.45) * np.cos(mid_angle) + x0
mid_angle_y = (r+0.45) * np.sin(mid_angle) + y0

angle_value = round( np.rad2deg(abs(theta_1-theta_2)), 2)

plt.text(mid_angle_x, mid_angle_y, angle_value, fontsize=8)

plt.show()