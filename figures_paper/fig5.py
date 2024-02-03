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



def delta_A_g(delta_A_r: float) -> float:
      return l_r / l_g * k_dispersion(l_g) / k_dispersion(l_r) * delta_A_r


print(f"delta_g = {round(l_r / l_g * k_dispersion(l_g) / k_dispersion(l_r), ndigits=3)} x delta_r")

def delta_A_b(delta_A_r: float) -> float:
      return l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r) * delta_A_r

print(f"delta_b = {round(l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r), ndigits=3)} x delta_r")
delta_A_r_1 = np.arange(0*np.pi, 10*np.pi, 0.001)
delta_R_r_1 = np.array([R_pi(d) for d in delta_A_r_1])
delta_R_g_1 = np.array([R_pi(delta_A_g(d)) for d in delta_A_r_1])
delta_R_b_1 = np.array([R_pi(delta_A_b(d)) for d in delta_A_r_1])

delta_A_r_2 = np.arange(10*np.pi, 20*np.pi, 0.001)
delta_R_r_2 = np.array([R_pi(d) for d in delta_A_r_2])
delta_R_g_2 = np.array([R_pi(delta_A_g(d)) for d in delta_A_r_2])
delta_R_b_2 = np.array([R_pi(delta_A_b(d)) for d in delta_A_r_2])

fig, (ax1, ax2) = plt.subplots(2,1, sharex=False, figsize = (6,2.5))

ax1.plot(delta_A_r_1, delta_R_r_1, color="red", label=r"$\tilde{\delta}_r=R_{\pi}(\delta_r)$")
ax1.plot(delta_A_r_1, delta_R_g_1, color="green", label=r"$\tilde{\delta}_g=R_{\pi}(\delta_g)$")
ax1.plot(delta_A_r_1, delta_R_b_1, color="blue", label=r"$\tilde{\delta}_b=R_{\pi}(\delta_b)$")

ax2.plot(delta_A_r_2, delta_R_r_2, color="red", )
ax2.plot(delta_A_r_2, delta_R_g_2, color="green", )
ax2.plot(delta_A_r_2, delta_R_b_2, color="blue", )

for ax in (ax1, ax2):
      ax.grid(True)
      ax.set_aspect(1.0)
      ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi))
      ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi/2))
      ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

      ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
      ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 6))
      ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))
      ax.set_ylabel(r'$\tilde{\delta}$', fontsize=12)
      ax.set_xlabel(r'$\delta_r$', fontsize=12)

#
# ax1.plot([6*math.pi, 6*math.pi], [0, math.pi], color="black", linestyle='solid', linewidth=1.5)
# # ax2.plot([12*math.pi, 12*math.pi], [0, math.pi], color="black", linestyle='dotted', linewidth=1.5)
# # ax2.plot([18*math.pi, 18*math.pi], [0, math.pi], color="black", linestyle='dotted', linewidth=1.5)
# ax2.plot([20*math.pi, 20*math.pi], [0, math.pi], color="black", linestyle='solid', linewidth=1.5)

ax1.legend()



ax1.legend( ncol=3, loc=(0.05, 1.02), fontsize=10)

plt.subplots_adjust(wspace=0, hspace=0)
plt.savefig('Fig5.tiff', format='tiff', dpi=2000, bbox_inches='tight')

plt.show()
