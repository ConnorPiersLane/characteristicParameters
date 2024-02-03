import math
import numpy as np
import matplotlib.pyplot as plt
import pi_axis_plotter
from charpar.linear import R_pi
from charpar.rgb import generate_dispersion_function_k

rc = {"font.family" : "serif",
      "mathtext.fontset" : "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

# CIE RGB color space




def delta_A_g(delta_A_r: float) -> float:
      return (4/3) * delta_A_r


delta_A_r = np.arange(0.0, 7*np.pi, 0.001)
delta_R_r = np.array([R_pi(d) for d in delta_A_r])
delta_R_g = np.array([R_pi(delta_A_g(d)) for d in delta_A_r])

fig, ax = plt.subplots()
ax.grid(True)
ax.set_aspect(1.0)
ax.axhline(0, color='black', lw=2)
ax.axvline(0, color='black', lw=2)

ax.plot(delta_A_r, delta_R_r, color="red", label=r"$\tilde{\delta}_r=R_{\pi}(\delta_r)$")
ax.plot(delta_A_r, delta_R_g, color="green", label=r"$\tilde{\delta}_g=R_{\pi}(\delta_g)$")


ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

x = [math.pi/2, 6*math.pi-math.pi/2, 6*math.pi+math.pi/2]

ax.plot(x,[R_pi(d) for d in x], 'ko', markersize=5)
ax.plot(x,[R_pi(delta_A_g(d)) for d in x], 'ko', markersize=5)
ax.plot([3*math.pi, 3*math.pi], [0, math.pi], color="black", linestyle='solid', linewidth=1.5)
#ax.plot([6*math.pi, 6*math.pi], [0, math.pi], color="black", linestyle='dotted', linewidth=1.5)


plt.xticks(size = 12)
plt.yticks(size = 14)
ax.legend()

plt.xlabel(r'$\delta_r$', fontsize=14)
plt.ylabel(r'$\tilde{\delta}$', fontsize=14)
plt.legend( ncol=3, loc=(0.05, 1.02), fontsize=10)
plt.savefig('Fig3.tiff', format='tiff', dpi=2000, bbox_inches='tight')

plt.show()
