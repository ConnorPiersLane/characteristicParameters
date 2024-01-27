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

l_r = 700
l_g = 546.1
l_b = 435.8


k_dispersion = generate_dispersion_function_k(lambda_0=632.8, a = 25.5e3, b = 3.25e9)

delta_A_r = np.arange(0.0, 6*np.pi, 0.001)

def delta_A_g(delta_A_r: float) -> float:
      return l_r / l_g * k_dispersion(l_g) / k_dispersion(l_r) * delta_A_r

def delta_A_b(delta_A_r: float) -> float:
      return l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r) * delta_A_r

delta_A_r_actual = 9*math.pi/2
delta_R_r_measured = R_pi(delta_A_r_actual)
delta_R_g_measured = R_pi(delta_A_g(delta_A_r_actual))
delta_R_b_measured = R_pi(delta_A_b(delta_A_r_actual))

delta_A_r = np.arange(0.0, 6*np.pi, 0.001)
delta_R_r = np.array([R_pi(d) for d in delta_A_r])
delta_R_g = np.array([R_pi(delta_A_g(d)) for d in delta_A_r])
delta_R_b = np.array([R_pi(delta_A_b(d)) for d in delta_A_r])

plt.plot(delta_A_r, delta_R_r, color="red", label=r"$\tilde{\delta}_r=R_{\pi}(\delta_r)$")
plt.plot(delta_A_r, delta_R_g, color="green", label=r"$\tilde{\delta}_g=R_{\pi}(\delta_g)$")
plt.plot(delta_A_r, delta_R_b, color="blue", label=r"$\tilde{\delta}_b=R_{\pi}(\delta_b)$")

ax = plt.gca()
ax.grid(True)
ax.set_aspect(1.0)
ax.axhline(0, color='black', lw=2)
ax.axvline(0, color='black', lw=2)
ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.legend()

plt.xlabel(r'$\delta_r$', fontsize=12)
plt.ylabel(r'$\tilde{\delta}$', fontsize=12)
plt.legend( ncol=3, loc=(0.05, 1.02))
plt.savefig('Fig4.tiff', format='tiff', dpi=2000, bbox_inches='tight')

plt.show()
