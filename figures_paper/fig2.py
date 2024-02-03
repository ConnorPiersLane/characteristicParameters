import numpy as np
import matplotlib.pyplot as plt
import pi_axis_plotter

from charpar.linear import R_pi
from charpar.circular import R_pi_2

rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

delta = np.arange(0, 2 * np.pi, 0.001)
delta_R_linear = np.array([R_pi(d) for d in delta])
delta_R_circ = np.array([R_pi_2(d) for d in delta])



fig, ax = plt.subplots()
ax.grid(True)
ax.set_aspect(1.0)
ax.axhline(0, color='black', lw=2)
ax.axvline(0, color='black', lw=2)

ax.plot(delta, delta_R_linear, label=r'$R_{\pi}(\delta)$', linewidth=2)
ax.plot(delta, delta_R_circ, label=r'$R_{\pi/2}(\delta)$', linestyle="dashed", linewidth=2)

ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))
plt.xticks(size = 20)
plt.yticks(size = 20)
plt.xlabel(r'$\delta$', fontsize=20)
plt.ylabel(r'$\tilde{\delta}$', fontsize=20)
plt.legend(ncol=2, loc=(0.05, 1.02), fontsize=20)
plt.savefig('Fig2.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()
