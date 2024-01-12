import math
import pickle
import matplotlib.pyplot as plt
import numpy as np

import pi_axis_plotter

rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

with open('measured_values_fig3.pickle', 'rb') as handle:
    measured_values = pickle.load(handle)

with open('true_values_fig3.pickle', 'rb') as handle:
    true_values = pickle.load(handle)

X_delta = []
Y_delta = []

X_theta = []
Y_theta = []
X_theta_tildeed = []
Y_theta_tildeed = []

X_omega = []
Y_omega = []
X_omega_tildeed = []
Y_omega_tildeed = []

delta = []
delta_U = []
delta_V = []
theta_U = []
theta_V = []
theta_U_tildeed = []
theta_V_tildeed = []
omega_U = []
omega_V = []
omega_U_tildeed= []
omega_V_tildeed = []


for (charpara, true_value) in zip(measured_values, true_values):
    value = true_value
    # Delta
    X_delta.append(value[0])
    Y_delta.append(value[2])
    delta.append(charpara.delta_tilde)
    delta_U.append(math.cos(charpara.delta_tilde))
    delta_V.append(math.sin(charpara.delta_tilde))

    # Theta
    theta_tilde = charpara.theta_tilde % (math.pi / 2)
    if math.isclose(true_value[0], 0) or math.isclose(true_value[0], math.pi) or math.isclose(true_value[0], 2*math.pi):
        X_theta_tildeed.append(value[0])
        Y_theta_tildeed.append(value[2])
        theta_U_tildeed.append(math.cos(theta_tilde))
        theta_V_tildeed.append(math.sin(theta_tilde))
    else:
        X_theta.append(value[0])
        Y_theta.append(value[2])
        theta_U.append(math.cos(theta_tilde))
        theta_V.append(math.sin(theta_tilde))

    # Omega
    omega_i = charpara.omega_tilde % math.pi
    if math.isclose(omega_i, math.pi):
        omega_i = 0
    if math.isclose(true_value[0], math.pi):
        X_omega_tildeed.append(value[0])
        Y_omega_tildeed.append(value[2])
        omega_U_tildeed.append(math.cos(omega_i))
        omega_V_tildeed.append(math.sin(omega_i))
    else:
        X_omega.append(value[0])
        Y_omega.append(value[2])
        omega_U.append(math.cos(omega_i))
        omega_V.append(math.sin(omega_i))


fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=True)

ax1.quiver(X_delta, Y_delta, delta_U, delta_V, color="k", pivot="mid", width=0.006, scale=20, headlength=3,headaxislength=3)

ax2.quiver(X_theta, Y_theta, theta_U, theta_V, color="k", pivot="mid", width=0.006, scale=20, headlength=3,headaxislength=3)
ax2.quiver(X_theta_tildeed, Y_theta_tildeed, theta_U_tildeed, theta_V_tildeed, color='red', pivot="mid", width=0.007, scale=20, headlength=3, headaxislength=3)

ax3.quiver(X_omega, Y_omega, omega_U, omega_V, color="k", pivot="mid", width=0.006, scale=20, headlength=3,headaxislength=3)
ax3.quiver(X_omega_tildeed, Y_omega_tildeed, omega_U_tildeed, omega_V_tildeed, color='red', pivot="mid", width=0.007, scale=20, headlength=3, headaxislength=3)

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

plt.savefig('Fig3.tiff', format='tiff', dpi=2000)
plt.show()
