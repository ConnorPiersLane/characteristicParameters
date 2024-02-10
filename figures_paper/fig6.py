import numpy as np

from section3_2_data import *
import pi_axis_plotter


delta_r_plotting = np.arange(0, 26 * np.pi, 0.001)
res = [L([x,x+0.25*math.pi]) for x in delta_r_plotting]

fig, ax = plt.subplots(figsize = (6,2))



ax.grid(True)
# ax.axvline(5*math.pi, color='black', lw=2, linestyle='dashed')
# ax.axvline(12*math.pi, color='black', lw=2, linestyle='dotted')
# ax.axvline(18*math.pi, color='black', lw=2, linestyle='dotted')
# ax.axvline(25*math.pi, color='black', lw=2, linestyle='dashed')
# ax.axhline(0, color='black', lw=2)
# ax.axvline(0, color='black', lw=2)
ax.xaxis.set_major_locator(plt.MultipleLocator(2*np.pi))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(4)))

ax.plot(delta_r_plotting, res,)
#ax.plot(result1.x[0], L([result1.x[0], result1.x[1]]), 'rx', markersize=10)
# ax.plot(result2.x[0], L([result2.x[0], result2.x[1]]), 'rx', markersize=15, linewidth=2)
ax.set_ylim([0, 2.25*math.pi])
ax.set_xlim([0, 25 * math.pi])

print(round(result1.x[0]/math.pi, ndigits=2))
print(round(result2.x[0]/math.pi, ndigits=2))
plt.xticks(size = 12)
plt.yticks(size = 12)
plt.xlabel(r'$\delta_{r1}$', fontsize=12)
plt.ylabel(r'$L$', fontsize=12)
plt.savefig('Fig6.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()