import math
import numpy as np
import matplotlib.pyplot as plt
import pi_axis_plotter
from charpar.linear import R_pi
from charpar.rgb import generate_dispersion_function_k, generate_linear_residual_vector_norm, generate_rgb_optimizer

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




def delta_A_b(delta_A_r: float) -> float:
      return l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r) * delta_A_r

delta_A_r =13.5*math.pi
delta_r = round(R_pi(delta_A_r), ndigits=1)
delta_g = round(R_pi(delta_A_g(delta_A_r)), ndigits=1)
delta_b = round(R_pi(delta_A_b(delta_A_r)), ndigits=1)
print(f"delta_r = {delta_r}")
print(f"delta_g = {delta_g}")
print(f"delta_b = {delta_b}")

residual_norm = generate_linear_residual_vector_norm(
      measured_relative_phases=[delta_r,delta_g,delta_b],
      wavelengths=[l_r, l_g, l_b],
      reduced_dispersion_function=k_dispersion
)

optimizer1 = generate_rgb_optimizer(ub_delta=6*math.pi)
optimizer2 = generate_rgb_optimizer(ub_delta=20*math.pi)
result1 = optimizer1(residual_norm)
result2 = optimizer2(residual_norm)


delta_r_plotting = np.arange(0, 20 * np.pi, 0.001)
res = [residual_norm(x) for x in delta_r_plotting]

fig, ax = plt.subplots()



ax.grid(True)
ax.axvline(6*math.pi, color='black', lw=2, linestyle='dashed')
# ax.axvline(12*math.pi, color='black', lw=2, linestyle='dotted')
# ax.axvline(18*math.pi, color='black', lw=2, linestyle='dotted')
ax.axvline(20*math.pi, color='black', lw=2, linestyle='dashed')
ax.axhline(0, color='black', lw=2)
ax.axvline(0, color='black', lw=2)
ax.xaxis.set_major_locator(plt.MultipleLocator(2*np.pi))
ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi))
ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 4))
ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(4)))

ax.plot(delta_r_plotting, res,)
ax.plot(result1.x[0], residual_norm(result1.x[0]), 'rx', markersize=10)
ax.plot(result2.x[0], residual_norm(result2.x[0]), 'rx', markersize=15, linewidth=2)


print(round(result1.x[0]/math.pi, ndigits=2))
print(round(result2.x[0]/math.pi, ndigits=2))
plt.xticks(size = 16)
plt.yticks(size = 16)
plt.xlabel(r'$\delta_r$', fontsize=16)
plt.ylabel(r'$|r|$', fontsize=16)
plt.savefig('Fig6.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()