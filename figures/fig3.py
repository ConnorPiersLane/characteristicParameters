import math
import numpy as np
import matplotlib.pyplot as plt
import pi_axis_plotter
from characteristicParameters.triangle_wave_functions import T_pi

# Formatting matplotlib
rc = {"font.family" : "serif",
      "mathtext.fontset" : "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]


# Define relationship delta_g - delta_r
def delta_g(delta_r: float) -> float:
      return (4/3) * delta_r

# x axis
delta_r = np.arange(0.0, 7*np.pi, 0.001)

# y axis
delta_r_tilde = np.array([T_pi(d) for d in delta_r])
delta_g_tilde = np.array([T_pi(delta_g(d)) for d in delta_r])

# Plot the results
fig, ax = plt.subplots()
ax.grid(True)
ax.set_aspect(1.0)

ax.plot(delta_r, delta_r_tilde, color="red", label=r"$\tilde{\delta}_r=T_{\pi}(\delta_r)$")
ax.plot(delta_r, delta_g_tilde, color="green", label=r"$\tilde{\delta}_g=T_{\pi}(\delta_g)$")

ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

# Plot the black dots and black
x = [math.pi/2, 6*math.pi-math.pi/2, 6*math.pi+math.pi/2]

ax.plot(x,[T_pi(d) for d in x], 'ko', markersize=6)
ax.plot(x, [T_pi(delta_g(d)) for d in x], 'ko', markersize=6)
ax.plot([3*math.pi, 3*math.pi], [0, math.pi], color="black", linestyle='solid', linewidth=1.5)
ax.set_ylim([0, math.pi])
ax.set_xlim([0, 6.75 * math.pi])

d = 5/2*math.pi
x=[d]
ax.plot(x,[T_pi(d) for d in x], 'kx', markersize=6)
ax.plot(x, [T_pi(delta_g(d)) for d in x], 'kx', markersize=6)
d = 7/2*math.pi
x=[d]
ax.plot(x,[T_pi(d) for d in x], 'kx', markersize=6)
ax.plot(x, [T_pi(delta_g(d)) for d in x], 'kx', markersize=6)

plt.xticks(size = 12)
plt.yticks(size = 12)
ax.legend()

plt.xlabel(r'$\delta_r$', fontsize=14)
plt.ylabel(r'$\tilde{\delta}_{r,g}$', fontsize=14)
plt.legend( ncol=3, loc=(0.05, 1.02), fontsize=10)
plt.savefig('Fig3.tiff', format='tiff', dpi=2000, bbox_inches='tight')

plt.show()
