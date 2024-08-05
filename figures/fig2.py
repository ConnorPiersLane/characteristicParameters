import math

import matplotlib.pyplot as plt
import numpy as np
from characteristicParameters.triangle_wave_functions import T_pi
from characteristicParameters.triangle_wave_functions import T_pi_2

import pi_axis_plotter

# Formatting matplotlib
rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

# x axis
delta = np.arange(0, 4 * np.pi, 0.001)

# y axis
delta_R_linear = np.array([T_pi(d) for d in delta])
delta_R_circ = np.array([T_pi_2(d) for d in delta])

# Plot the results
fig, ax = plt.subplots()
ax.grid(True)
ax.set_aspect(1.0)

ax.plot(delta, delta_R_linear, label=r'$T_{\pi}(\delta)$', linewidth=2)
ax.plot(delta, delta_R_circ, label=r'$T_{\pi/2}(\delta)$', linestyle="dashed", linewidth=2)

ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))
ax.set_ylim([0, math.pi])
ax.set_xlim([0, 4 * math.pi])

plt.xticks(size=20)
plt.yticks(size=20)
plt.xlabel(r'$\delta$', fontsize=20)
plt.ylabel(r'$\tilde{\delta}$', fontsize=20)
plt.legend(ncol=2, loc=(0.05, 1.02), fontsize=20)
plt.savefig('Fig2.tiff', format='tiff', dpi=1000, bbox_inches='tight')
plt.show()
