import math

import matplotlib.pyplot as plt
from characteristicParameters import rgbMethod
from characteristicParameters.triangle_wave_functions import T_pi

rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

# Define the wavelengths:
l_r = 632.8
l_g = 546.1
l_b = 435.8

# Eq. (4) in the Paper
k_function = rgbMethod.define_reduced_birefringence_function(lambda_0=632.8, a=25.5e3, b=3.25e9)

#
def delta_g(delta_r: float) -> float:
    return rgbMethod.convert_retardation_to_different_wavelength(k_function=k_function,
                                                                  wavelength_1=l_r,
                                                                  delta_1=delta_r,
                                                                  wavelength_2=l_g)


def delta_b(delta_r: float) -> float:
    return rgbMethod.convert_retardation_to_different_wavelength(k_function=k_function,
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

measurement1 = rgbMethod.MeasuredRetardationsAtOneLocation(
    measurement_at_reference_wavelength=       rgbMethod.RetardationMeasurement(wavelength=l_r, delta=delta_r_1_tilde),
       additional_measurements=[rgbMethod.RetardationMeasurement(wavelength=l_g, delta=delta_g_1_tilde),
                                rgbMethod.RetardationMeasurement(wavelength=l_b, delta=delta_b_1_tilde)],
    reduced_birefringence_function=k_function)

measurement2 = rgbMethod.MeasuredRetardationsAtOneLocation(
    measurement_at_reference_wavelength=        rgbMethod.RetardationMeasurement(wavelength=l_r, delta=delta_r_2_tilde),
    additional_measurements= [rgbMethod.RetardationMeasurement(wavelength=l_g, delta=delta_g_2_tilde),
                              rgbMethod.RetardationMeasurement(wavelength=l_b, delta=delta_b_2_tilde)],
    reduced_birefringence_function=k_function)


multi_locations = rgbMethod.MultipleNeighboringLocations(neighboring_locations=[measurement1, measurement2])

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