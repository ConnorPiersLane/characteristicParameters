import numpy as np

import math

import matplotlib.pyplot as plt



from opeqmo.triangle_wave_functions import T_pi
from opeqmo import rgb_method

rc = {"font.family" : "serif",
      "mathtext.fontset" : "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

# CIE rgb_method color space

l_r = 632.8
l_g = 546.1
l_b = 435.8
# l_r = 610
# l_g = 545
# l_b = 435

k_dispersion = rgb_method.define_reduced_birefringence_function(lambda_0=632.8, a = 25.5e3, b = 3.25e9)



def delta_A_g(delta_A_r: float) -> float:
      return l_r / l_g * k_dispersion(l_g) / k_dispersion(l_r) * delta_A_r


def delta_A_b(delta_A_r: float) -> float:
      return l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r) * delta_A_r

print(f"delta_g = {round(l_r / l_g * k_dispersion(l_g) / k_dispersion(l_r), ndigits=2)} x delta_r")
print(f"delta_g = {round(l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r), ndigits=2)} x delta_r")


delta_A_r_1 = 21.5*math.pi
delta_A_r_2 = 21.75*math.pi
delta_A_r_3 = 21.1*math.pi
delta_r_1 = round(T_pi(delta_A_r_1), ndigits=2)
delta_g_1 = round(T_pi(delta_A_g(delta_A_r_1)), ndigits=2)
delta_b_1 = round(T_pi(delta_A_b(delta_A_r_1)), ndigits=2)
print("One:")
print(f"delta_r = {delta_r_1}")
print(f"delta_g = {delta_g_1}")
print(f"delta_b = {delta_b_1}")
print("Two:")
delta_r_2 = round(T_pi(delta_A_r_2), ndigits=2)
delta_g_2 = round(T_pi(delta_A_g(delta_A_r_2)), ndigits=2)
delta_b_2 = round(T_pi(delta_A_b(delta_A_r_2)), ndigits=2)
print(f"delta_r = {delta_r_2}")
print(f"delta_g = {delta_g_2}")
print(f"delta_b = {delta_b_2}")


E_1 = rgb_method.define_error_function_E(
      measured_relative_phases=[delta_r_1,delta_g_1,delta_b_1],
      wavelengths=[l_r, l_g, l_b],
      reduced_birefringence_function=k_dispersion
)
E_2 = rgb_method.define_error_function_E(
      measured_relative_phases=[delta_r_2,delta_g_2,delta_b_2],
      wavelengths=[l_r, l_g, l_b],
      reduced_birefringence_function=k_dispersion
)
L = rgb_method.generate_cost_function_L([E_1, E_2], K=1)

optimizer1 = rgb_method.define_function_that_finds_minimum_of_E_and_J_function(n_parameters=2, ub_delta=5 * math.pi)
optimizer2 = rgb_method.define_function_that_finds_minimum_of_E_and_J_function(n_parameters=2, ub_delta=25 * math.pi)
result1 = optimizer1(L)
result2 = optimizer2(L)

print(f"delta_r1 = {result1.x[0]/math.pi}, delta_r2 = {result1.x[1]/math.pi}")
print(f"delta_r1 = {result2.x[0]/math.pi}, delta_r2 = {result2.x[1]/math.pi}")

from figures_main_paper import pi_axis_plotter
delta_r_plotting = np.arange(0, 26 * np.pi, 0.001)
res1 = [E_1(x) for x in delta_r_plotting]
res2 = [E_2(x) for x in delta_r_plotting]
res = [L([x,x+0.25*math.pi]) for x in delta_r_plotting]


fig, (ax1, ax2, ax3) = plt.subplots(3,1, )

ax1.plot(delta_r_plotting, res1,)
ax2.plot(delta_r_plotting, res2,)
ax3.plot(delta_r_plotting, res,)
#ax.plot(result1.x[0], L([result1.x[0], result1.x[1]]), 'rx', markersize=10)
ax3.plot(result2.x[0], L([result2.x[0], result2.x[1]]), 'rx', markersize=6, linewidth=4)

for ax in (ax1, ax2, ax3):
    ax.grid(True)
    # ax.axvline(5*math.pi, color='black', lw=2, linestyle='dashed')
    # #
    # # ax.axvline(25*math.pi, color='black', lw=2, linestyle='dashed')
    # ax.axhline(0, color='black', lw=2)
    # ax.axvline(0, color='black', lw=2)
    ax.xaxis.set_major_locator(plt.MultipleLocator(2*np.pi))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

    if ax == ax3:
        ax.set_ylim([0, 2.25 * math.pi])
    else:
        ax.set_ylim([0, 1.25*math.pi])

    ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
    ax.set_xlim([0, 25 * math.pi])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(4)))

ax1.set_ylabel(r'$E_1$', fontsize=12)
ax1.set_xlabel(r'$\delta_{r1}$', fontsize=12)
ax2.set_ylabel(r'$E_2$', fontsize=12)
ax2.set_xlabel(r'$\delta_{r2}$', fontsize=12)
ax3.set_ylabel(r'$L$', fontsize=12)
ax3.set_xlabel(r'$\delta_{r1}, \delta_{r2}-0.25\pi$', fontsize=12)

plt.subplots_adjust(wspace=0, hspace=0.6)

plt.savefig('Fig6.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()