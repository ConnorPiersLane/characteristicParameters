import numpy as np
import math
import matplotlib.pyplot as plt

from oem.triangle_wave_functions import T_pi
from oem import rgb_method

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
                                                                  wavelength_old=l_r,
                                                                  delta_old=delta_r,
                                                                  wavelength_new=l_g)


def delta_b(delta_r: float) -> float:
    return rgb_method.convert_retardation_to_different_wavelength(k_function=k_function,
                                                                  wavelength_old=l_r,
                                                                  delta_old=delta_r,
                                                                  wavelength_new=l_b)


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

measurement1 = rgb_method.OneLocation(
    lambda_delta_r=       rgb_method.LambdaAndDelta(wavelength=l_r, delta=delta_r_1_tilde),
       additional_lambda_deltas=[rgb_method.LambdaAndDelta(wavelength=l_g, delta=delta_g_1_tilde),
                                 rgb_method.LambdaAndDelta(wavelength=l_b, delta=delta_b_1_tilde)],
    reduced_birefringence_function=k_function)

measurement2 = rgb_method.OneLocation(
    lambda_delta_r=        rgb_method.LambdaAndDelta(wavelength=l_r, delta=delta_r_2_tilde),
    additional_lambda_deltas= [rgb_method.LambdaAndDelta(wavelength=l_g, delta=delta_g_2_tilde),
                               rgb_method.LambdaAndDelta(wavelength=l_b, delta=delta_b_2_tilde)],
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


from figures_main_paper import pi_axis_plotter

x = np.arange(20 * np.pi, 24 * np.pi, 0.05)
y = np.arange(-2*np.pi, 2 * np.pi, 0.05)
X, Y = np.meshgrid(x, y)
Z = np.array([[L([xx, xx+yy]) for xx in x] for yy in y])

# Plot the surface.
from matplotlib import cm
fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm, antialiased=False)
# plt.savefig('Fig7.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()
