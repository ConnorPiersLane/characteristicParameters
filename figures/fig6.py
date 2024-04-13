import numpy as np
import math
import matplotlib.pyplot as plt

from characteristicParameters.triangle_wave_functions import T_pi
from characteristicParameters import rgbMethod

rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

# Define the wavelengths:
l_r = 632.8
l_g = 546.1
l_b = 435.8

# Eq. (4) in the Paper
k_function = rgb_method.define_reduced_birefringence_function(lambda_0=632.8, a=25.5e3, b=3.25e9)

#
def delta_g(delta_r: float) -> float:
    return rgb_method.convert_retardation_to_different_wavelength(k_function=k_function,
                                                                  wavelength_1=l_r,
                                                                  delta_1=delta_r,
                                                                  wavelength_2=l_g)


def delta_b(delta_r: float) -> float:
    return rgb_method.convert_retardation_to_different_wavelength(k_function=k_function,
                                                                  wavelength_1=l_r,
                                                                  delta_1=delta_r,
                                                                  wavelength_2=l_b)


# Plot the approximate relation
print(f"delta_g = {round(l_r / l_g * k_function(l_g) / k_function(l_r), ndigits=2)} x delta_r")
print(f"delta_g = {round(l_r / l_b * k_function(l_b) / k_function(l_r), ndigits=2)} x delta_r")

# We will be looking for these two points:
delta_r_1 = 21.25 * math.pi
difference = math.pi/2
delta_r_2 = delta_r_1+difference
delta_r_1_tilde = round(T_pi(delta_r_1), ndigits=2)

delta_g_1_tilde = round(T_pi(delta_g(delta_r_1)), ndigits=2)
delta_b_1_tilde = round(T_pi(delta_b(delta_r_1)), ndigits=2)
print("Measured Retardations:"
      "")
print("One:")
print(f"delta_r = {delta_r_1_tilde}")
print(f"delta_g = {delta_g_1_tilde}")
print(f"delta_b = {delta_b_1_tilde}")
print("Two:")
delta_r_2_tilde = round(T_pi(delta_r_2), ndigits=2)
delta_g_2_tilde = round(T_pi(delta_g(delta_r_2)), ndigits=2)
delta_b_2_tilde = round(T_pi(delta_b(delta_r_2)), ndigits=2)
print(f"delta_r = {delta_r_2_tilde}")
print(f"delta_g = {delta_g_2_tilde}")
print(f"delta_b = {delta_b_2_tilde}")

measurement1 = rgb_method.MeasuredRetardationsAtOneLocation(
    measurement_at_reference_wavelength=       rgb_method.RetardationMeasurement(wavelength=l_r, delta=delta_r_1_tilde),
       additional_measurements=[rgb_method.RetardationMeasurement(wavelength=l_g, delta=delta_g_1_tilde),
                                rgb_method.RetardationMeasurement(wavelength=l_b, delta=delta_b_1_tilde)],
    reduced_birefringence_function=k_function)

measurement2 = rgb_method.MeasuredRetardationsAtOneLocation(
    measurement_at_reference_wavelength=        rgb_method.RetardationMeasurement(wavelength=l_r, delta=delta_r_2_tilde),
    additional_measurements= [rgb_method.RetardationMeasurement(wavelength=l_g, delta=delta_g_2_tilde),
                              rgb_method.RetardationMeasurement(wavelength=l_b, delta=delta_b_2_tilde)],
    reduced_birefringence_function=k_function)


multi_locations = rgb_method.MultipleNeighboringLocations(neighboring_locations=[measurement1, measurement2])

# Error functions 1 and 2:
def E1(delta: float):
    return measurement1.error_function_E(delta)

def E2(delta: float):
    return measurement2.error_function_E(delta)

# collective error function
k_value = 0.1
def L(deltas: list[float, float]):
    return multi_locations.collective_error_function_L(delta_rs=deltas, k=k_value)

deltas_found = multi_locations.find_all_neighboring_delta_r(k=k_value,
                                                            lb_delta=0,
                                                            ub_delta=25*math.pi,
                                                            strategy="rand2exp")

print(f"delta_r1 = {deltas_found[0] / math.pi}, delta_r2 = {deltas_found[1] / math.pi}")


from figures import pi_axis_plotter

delta_r_plotting = np.arange(0, 26 * np.pi, 0.001)
res1 = [E1(x) for x in delta_r_plotting]
res2 = [E2(x) for x in delta_r_plotting]
res = [L([x, x + difference]) for x in delta_r_plotting]

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, )

ax1.plot(delta_r_plotting, res1, )
ax2.plot(delta_r_plotting, res2, )
ax3.plot(delta_r_plotting, res, )
# ax.plot(result1.x[0], L([result1.x[0], result1.x[1]]), 'rx', markersize=10)
ax3.plot(deltas_found[0], L([deltas_found[0], deltas_found[1]]), 'rx', markersize=6, linewidth=4)

for ax in (ax1, ax2, ax3):
    ax.grid(True)
    # ax.axvline(5*math.pi, color='black', lw=2, linestyle='dashed')
    # #
    # # ax.axvline(25*math.pi, color='black', lw=2, linestyle='dashed')
    # ax.axhline(0, color='black', lw=2)
    # ax.axvline(0, color='black', lw=2)
    ax.xaxis.set_major_locator(plt.MultipleLocator(2 * np.pi))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

    if ax == ax3:
        ax.set_ylim([-0.25*math.pi, 2.25 * math.pi])
    else:
        ax.set_ylim([0, 1.25 * math.pi])

    ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 4))
    ax.set_xlim([0, 25 * math.pi])
    ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(4)))

ax1.set_ylabel(r'$E_1$', fontsize=12)
ax1.set_xlabel(r'$\delta_{r1}$', fontsize=12)
ax2.set_ylabel(r'$E_2$', fontsize=12)
ax2.set_xlabel(r'$\delta_{r2}$', fontsize=12)
ax3.set_ylabel(r'$L$', fontsize=12)
ax3.set_xlabel(r'$\delta_{r1}, \delta_{r2}-\pi/2$', fontsize=12)

plt.subplots_adjust(wspace=0, hspace=0.6)

plt.savefig('Fig6.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()
