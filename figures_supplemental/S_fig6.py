import numpy as np

from figures_paper.section3_2_data import *
from figures_paper import pi_axis_plotter
delta_r_plotting = np.arange(0, 26 * np.pi, 0.001)
res1 = [E_1(x) for x in delta_r_plotting]
res2 = [E_2(x) for x in delta_r_plotting]



fig, (ax1, ax2) = plt.subplots(2,1, )

ax1.plot(delta_r_plotting, res1,)
ax2.plot(delta_r_plotting, res2,)

for ax in (ax1, ax2):
    ax.grid(True)
    # ax.axvline(5*math.pi, color='black', lw=2, linestyle='dashed')
    # #
    # # ax.axvline(25*math.pi, color='black', lw=2, linestyle='dashed')
    # ax.axhline(0, color='black', lw=2)
    # ax.axvline(0, color='black', lw=2)
    ax.xaxis.set_major_locator(plt.MultipleLocator(2*np.pi))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

    ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 4))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(4)))
    ax.set_ylim([0, math.pi])
    ax.set_xlim([0, 25*math.pi])

ax1.set_ylabel(r'$E_1$', fontsize=12)
ax1.set_xlabel(r'$\delta_{r1}$', fontsize=12)
ax2.set_ylabel(r'$E_2$', fontsize=12)
ax2.set_xlabel(r'$\delta_{r2}$', fontsize=12)
plt.subplots_adjust(wspace=0, hspace=0.4)

plt.savefig('S_Fig6.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()