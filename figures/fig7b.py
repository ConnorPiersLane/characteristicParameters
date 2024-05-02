from fig6_fig7_data import *

from figures import pi_axis_plotter

dx = 0.01

x = np.arange(20 * np.pi, 24 * np.pi + dx / 2, dx)
y = np.arange(20 * np.pi, 24 * np.pi + dx / 2, dx)
X, Y = np.meshgrid(x, y)
Z = np.array([[L([xx, yy]) for xx in x] for yy in y])

print(L([deltas_found[0], deltas_found[1]]))

dl = math.pi / 4
levels = np.arange(0, 3 * np.pi + dl / 2, dl)

fig, ax = plt.subplots(figsize=(6, 4))
CS = ax.contourf(X, Y, Z, levels=levels, cmap="viridis", extend="max")

ax.set_aspect(1.0)

ax.set_xlim([20 * np.pi, 24 * np.pi])
ax.set_ylim([20 * np.pi, 24 * np.pi])

ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))
ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.set_xlabel(r'$\delta_{r,1}$', fontsize=14)
ax.set_ylabel(r'$\delta_{r,2}$', fontsize=14)
ax.tick_params(axis='both', labelsize=12)

ax.plot(deltas_found[0], deltas_found[1], 'rx', markersize=8, linewidth=4)

linestyle = "dashed"
linestyle = "solid"
linewidth = 3
ax.plot([20 * math.pi, 20 * math.pi], [20 * math.pi, 24 * math.pi], color="black", linestyle=linestyle,
        linewidth=linewidth)
ax.plot([24 * math.pi, 24 * math.pi], [20 * math.pi, 24 * math.pi], color="black", linestyle=linestyle,
        linewidth=linewidth)
ax.plot([20 * math.pi, 24 * math.pi], [24 * math.pi, 24 * math.pi], color="black", linestyle=linestyle,
        linewidth=linewidth)
ax.plot([20 * math.pi, 24 * math.pi], [20 * math.pi, 20 * math.pi], color="black", linestyle=linestyle,
        linewidth=linewidth)

cbar = fig.colorbar(CS)
cbar.ax.set_ylabel(r'$L$', fontsize=12)

cbar.ax.set_yticks([0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi, 5 * math.pi / 2, 3 * math.pi])
cbar.ax.set_yticklabels(['0', r'$\frac{\pi}{2}$',
                         r'$\pi$', r'$\frac{3\pi}{2}$',
                         r'$2\pi$', r'$\frac{3\pi}{2}$',
                         r'$3\pi$'], fontsize=12)

plt.tight_layout()
plt.savefig('Fig7b.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()
