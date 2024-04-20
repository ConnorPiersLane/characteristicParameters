from fig6_fig7_data import *


from figures import pi_axis_plotter

x = np.arange(20 * np.pi, 24 * np.pi, 0.05)
y = np.arange(-2*np.pi, 2 * np.pi, 0.05)
X, Y = np.meshgrid(x, y)
Z = np.array([[L([xx, xx+yy]) for xx in x] for yy in y])

# Plot the surface.
from matplotlib import cm

fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=False)
plt.savefig('Fig7.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()
