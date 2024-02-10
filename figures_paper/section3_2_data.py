import math

import matplotlib.pyplot as plt



from charpar.linear import R_pi
from charpar import rgb

rc = {"font.family" : "serif",
      "mathtext.fontset" : "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

# CIE RGB color space

l_r = 632.8
l_g = 546.1
l_b = 435.8
# l_r = 610
# l_g = 545
# l_b = 435

k_dispersion = rgb.generate_dispersion_function_k(lambda_0=632.8, a = 25.5e3, b = 3.25e9)



def delta_A_g(delta_A_r: float) -> float:
      return l_r / l_g * k_dispersion(l_g) / k_dispersion(l_r) * delta_A_r


def delta_A_b(delta_A_r: float) -> float:
      return l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r) * delta_A_r

print(f"delta_g = {round(l_r / l_g * k_dispersion(l_g) / k_dispersion(l_r), ndigits=2)} x delta_r")
print(f"delta_g = {round(l_r / l_b * k_dispersion(l_b) / k_dispersion(l_r), ndigits=2)} x delta_r")


delta_A_r_1 = 21.5*math.pi
delta_A_r_2 = 21.75*math.pi
delta_r_1 = round(R_pi(delta_A_r_1), ndigits=2)
delta_g_1 = round(R_pi(delta_A_g(delta_A_r_1)), ndigits=2)
delta_b_1 = round(R_pi(delta_A_b(delta_A_r_1)), ndigits=2)
print("Zero:")
print(f"delta_r = {delta_r_1}")
print(f"delta_g = {delta_g_1}")
print(f"delta_b = {delta_b_1}")
print("One:")
delta_r_2 = round(R_pi(delta_A_r_2), ndigits=2)
delta_g_2 = round(R_pi(delta_A_g(delta_A_r_2)), ndigits=2)
delta_b_2 = round(R_pi(delta_A_b(delta_A_r_2)), ndigits=2)
print(f"delta_r = {delta_r_2}")
print(f"delta_g = {delta_g_2}")
print(f"delta_b = {delta_b_2}")

E_1 = rgb.generate_error_function_E(
      measured_relative_phases=[delta_r_1,delta_g_1,delta_b_1],
      wavelengths=[l_r, l_g, l_b],
      reduced_dispersion_function=k_dispersion
)
E_2 = rgb.generate_error_function_E(
      measured_relative_phases=[delta_r_2,delta_g_2,delta_b_2],
      wavelengths=[l_r, l_g, l_b],
      reduced_dispersion_function=k_dispersion
)
L = rgb.generate_cost_function_L([E_1, E_2], K=1)

optimizer1 = rgb.generate_rgb_optimizer(n_parameters=2, ub_delta=5*math.pi)
optimizer2 = rgb.generate_rgb_optimizer(n_parameters=2, ub_delta=25*math.pi)
result1 = optimizer1(L)
result2 = optimizer2(L)

print(f"delta_r1 = {result1.x[0]/math.pi}, delta_r2 = {result1.x[1]/math.pi}")
print(f"delta_r1 = {result2.x[0]/math.pi}, delta_r2 = {result2.x[1]/math.pi}")

# x = np.arange(0, 30 * np.pi, 0.1)
# y = np.arange(0, 30 * np.pi, 0.2)
# X, Y = np.meshgrid(x, y)
# R = []
# for y_i in y:
#       r = []
#       for x_i in x:
#             r.append(L([x_i, y_i]))
#       R.append(np.array(r))
# Z = np.array(R)
# # Plot the surface.
# fig, ax = plt.subplots(subplot_kw={"projection": "3d"})
# surf = ax.plot_surface(X, Y, Z, cmap=cm.coolwarm,
#                        linewidth=0, antialiased=False)
# ax.set_zlim(0, 10)
# plt.show()



