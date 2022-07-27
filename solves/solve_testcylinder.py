from computations import compute_vals
import matplotlib.pyplot as plt
from make_cylinder import cylinder
import numpy as np

x, y = cylinder()
n = len(x)
X, Y, theta, l = compute_vals(x, y)
x = np.append(x, x[0])
y = np.append(y, y[0])

print(x)
print(y)
print(X)
print(Y)
print(theta)
print(l)


fig, (ax1) = plt.subplots(1, constrained_layout=True)
ax1.plot(x, y)
ax1.set(xlabel='x', ylabel='y')
ax1.set_title(f"Circular Cylinder Profile with {n} Panels")
count = 0
for xitem,yitem in np.nditer([x,y]):
        etiqueta = "x_" + str(count)
        count += 1
        plt.annotate(etiqueta, (xitem,yitem), textcoords="offset points",xytext=(0,6),ha="center")
plt.show()