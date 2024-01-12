import math
import pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import ListedColormap

from charpar.linear import R_pi
from matplotlib.ticker import MultipleLocator


rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

with open('S_fig2_measured_values.pickle', 'rb') as handle:
    measured_values = pickle.load(handle)

with open('S_fig2_true_values.pickle', 'rb') as handle:
    true_values = pickle.load(handle)


ncol = 181  # because stepsize was 1° including omega=0° and omega=180°

delta_true = []
theta_true = []
omega_true = []

delta_tilde = []
theta_tilde = []
omega_tilde = []

for (measured_value, true_value) in zip(measured_values, true_values):
    delta_true.append(true_value[0])
    theta_true.append(true_value[1])
    omega_true.append(true_value[2])
    delta_tilde.append(measured_value[0])
    theta_tilde.append(measured_value[1])
    omega_tilde.append(measured_value[2])


def calc_color(diff) -> float:
    if diff < math.radians(1e-13):
        return 1
    elif diff < math.radians(1e-9):
        return 3
    elif diff < math.radians(1e-5):
        return 5
    else:
        return 7


delta_diff = []
theta_diff = []
omega_diff = []

for (true, fitted) in zip(delta_true, delta_tilde):
    true = R_pi(true)  # Measurement range is [0,\pi], hence we need to calculate the respective true relative value
    Diff = abs(true-fitted)
    color = calc_color(Diff)
    delta_diff.append(color)

for (true, fitted) in zip(theta_true, theta_tilde):
    fitted = fitted % (math.pi/2)  # Measuement range is [0,\pi/2), but fitted was within [0,\pi], hence the modulo
    true = true % (math.pi/2)  # In order to compare only the correct relative position, do the same with the true value
    Diff = abs(true-fitted)
    color = calc_color(Diff)
    theta_diff.append(color)

for (true, fitted) in zip(omega_true, omega_tilde):
    if math.isclose(true, math.pi):  #Omega is periodic with pi, meaning 0°==180°
        true = 0
    if math.isclose(fitted, math.pi):
        fitted = 0
    fitted = fitted % (math.pi)
    Diff = abs(true - fitted)
    color = calc_color(Diff)
    omega_diff.append(color)


# Change the arrays into an image
delta_img = np.flipud(np.reshape(delta_diff, (-1, ncol)).T)
theta_img = np.flipud(np.reshape(theta_diff, (-1, ncol)).T)
omega_img = np.flipud(np.reshape(omega_diff, (-1, ncol)).T)

delta_img = Image.fromarray(np.uint8(delta_img))
theta_img = Image.fromarray(np.uint8(theta_img))
omega_img = Image.fromarray(np.uint8(omega_img))

fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=False)

cmap = ListedColormap([ "whitesmoke", "grey", "black", "red"])
ax1.imshow(delta_img,  cmap=cmap, interpolation=None, vmin=0, vmax=8)
ax2.imshow(theta_img, cmap=cmap, interpolation=None, vmin=0, vmax=8)
ax3.imshow(omega_img, cmap=cmap, interpolation=None, vmin=0, vmax=8)


for ax in (ax1, ax2, ax3):
    ax.set_yticks((0, 180))
    ax.yaxis.set_minor_locator(MultipleLocator(90))
    ax.yaxis.set_ticklabels([r"$\pi$", "0"], fontsize=12)

    ax.set_ylabel(r"$\omega$", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    ax.set_xlabel(r"$\delta$, 6$\theta$", fontsize=12)

    ax.set_xticks((0, 180, 360, 540, round(4 * 180), round(5 * 180), round(6 * 180)))
    ax.xaxis.set_minor_locator(MultipleLocator(90))
    ax.xaxis.set_ticklabels(["0", r"$\pi$", r"$2\pi$", r"$3\pi$",
                              r"$4\pi$", r"$5\pi$", r"$6\pi$"])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


plt.savefig('S_Fig2.tiff', format='tiff', dpi=2000)

plt.show()



