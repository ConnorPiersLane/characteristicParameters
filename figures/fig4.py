import math
import pickle
import matplotlib.pyplot as plt
import numpy as np

import pi_axis_plotter
rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

# If not available, run fig4_generate_data.py first:
with open('data/measured_values_fig4.pickle', 'rb') as handle:
    measured_values = pickle.load(handle)

with open('data/true_values_fig4.pickle', 'rb') as handle:
    true_values = pickle.load(handle)

X_delta = []
Y_delta = []

X_theta = []
Y_theta = []
X_theta_red = []
Y_theta_red = []

X_omega = []
Y_omega = []
X_omega_red = []
Y_omega_red = []

delta = []
delta_U = []
delta_V = []
theta_U = []
theta_V = []
theta_U_red = []
theta_V_red = []
omega_U = []
omega_V = []
omega_U_red= []
omega_V_red = []


for (measured_value, true_value) in zip(measured_values, true_values):

    # X and Y Grid defined by the true values:
    X_delta.append(true_value[0])
    Y_delta.append(true_value[2])
    
    # Read the measured values
    delta_m = measured_value[0]
    theta_m = measured_value[1]
    omega_m = measured_value[2]

    # Delta
    delta.append(delta_m)
    delta_U.append(math.cos(delta_m))
    delta_V.append(math.sin(delta_m))

    # Theta
    # These quiver plots shall be red
    if math.isclose(true_value[0], 0) or math.isclose(true_value[0], math.pi) or math.isclose(true_value[0], 2*math.pi):
        X_theta_red.append(true_value[0])
        Y_theta_red.append(true_value[2])
        theta_U_red.append(math.cos(theta_m))
        theta_V_red.append(math.sin(theta_m))
    # These are not red
    else:
        X_theta.append(true_value[0])
        Y_theta.append(true_value[2])
        theta_U.append(math.cos(theta_m))
        theta_V.append(math.sin(theta_m))

    # Omega
    # These quiver plots shall be red
    if math.isclose(true_value[0], math.pi):
        X_omega_red.append(true_value[0])
        Y_omega_red.append(true_value[2])
        omega_U_red.append(math.cos(omega_m))
        omega_V_red.append(math.sin(omega_m))
    else:
        X_omega.append(true_value[0])
        Y_omega.append(true_value[2])
        omega_U.append(math.cos(omega_m))
        omega_V.append(math.sin(omega_m))

# Plot the results
fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)

# Delta
ax1.quiver(X_delta, Y_delta, delta_U, delta_V, color="k", pivot="mid", width=0.006, scale=20, headlength=3,headaxislength=3)

# Theta
ax2.quiver(X_theta, Y_theta, theta_U, theta_V, color="k", pivot="mid", width=0.006, scale=20, headlength=3,headaxislength=3)
ax2.quiver(X_theta_red, Y_theta_red, theta_U_red, theta_V_red, color='red', pivot="mid", width=0.007, scale=20, headlength=3, headaxislength=3)

# Omega
ax3.quiver(X_omega, Y_omega, omega_U, omega_V, color="k", pivot="mid", width=0.006, scale=20, headlength=3,headaxislength=3)
ax3.quiver(X_omega_red, Y_omega_red, omega_U_red, omega_V_red, color='red', pivot="mid", width=0.007, scale=20, headlength=3, headaxislength=3)

for ax in (ax1, ax2, ax3):
    ax.set_aspect(1.0)
    ax.xaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax.xaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
    ax.xaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))

    ax.yaxis.set_major_locator(plt.MultipleLocator(np.pi / 2))
    ax.yaxis.set_minor_locator(plt.MultipleLocator(np.pi / 12))
    ax.yaxis.set_major_formatter(plt.FuncFormatter(pi_axis_plotter.multiple_formatter(2)))
    ax.set_ylabel(r"$\omega$", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=12)

ax3.set_xlabel(r"$\delta$, 2$\theta$", fontsize=12)

plt.savefig('Fig4.tiff', format='tiff', dpi=2000)
plt.show()
