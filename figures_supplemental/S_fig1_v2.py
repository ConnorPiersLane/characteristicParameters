import math
import pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

from opeqmo.triangle_wave_functions import T_pi
from matplotlib.ticker import MultipleLocator


rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]



delta_img_all = []
theta_img_all = []
omega_img_all = []

eps = np.finfo(float).eps

leps = math.log10(eps)

for i in (1,2,3,4):
    with open(f'S_fig1_measured_values_{i}_L2norm.pickle', 'rb') as handle:
        measured_values = pickle.load(handle)

    with open('S_fig1_true_values.pickle', 'rb') as handle:
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


    delta_diff = []
    theta_diff = []
    omega_diff = []

    for (true, fitted) in zip(delta_true, delta_tilde):
        true = T_pi(true)  # Measurement range is [0,\pi], hence we need to calculate the respective true relative value
        Diff = abs(true-fitted)
        delta_diff.append(Diff)

    for (true, fitted) in zip(theta_true, theta_tilde):
        fitted = fitted % (math.pi/2)  # Measuement range is [0,\pi/2), but fitted was within [0,\pi], hence the modulo
        true = true % (math.pi/2)  # In order to compare only the correct relative position, do the same with the true value
        Diff = abs(true-fitted)
        theta_diff.append(Diff)

    for (true, fitted) in zip(omega_true, omega_tilde):
        if math.isclose(true, math.pi):  #Omega is periodic with pi, meaning 0°==180°
            true = 0
        if math.isclose(fitted, math.pi):
            fitted = 0
        fitted = fitted % (math.pi)
        Diff = abs(true - fitted)
        omega_diff.append(Diff)

    delta_diff_log = list(np.log10(delta_diff) / np.log10(eps))
    theta_diff_log = list(np.log10(theta_diff) / np.log10(eps))
    omega_diff_log = list(np.log10(omega_diff) / np.log10(eps))

    delta_diff_log_s = [i * 255 if i < 1 else 255 for i in delta_diff_log]
    theta_diff_log_s = [i * 255 if i < 1 else 255 for i in theta_diff_log]
    omega_diff_log_s = [i * 255 if i < 1 else 255 for i in omega_diff_log]

    # Change the arrays into an image
    delta_img = np.flipud(np.reshape(delta_diff_log_s, (-1, ncol)).T)
    theta_img = np.flipud(np.reshape(theta_diff_log_s, (-1, ncol)).T)
    omega_img = np.flipud(np.reshape(omega_diff_log_s, (-1, ncol)).T)

    delta_img = Image.fromarray(np.uint8(delta_img))
    theta_img = Image.fromarray(np.uint8(theta_img))
    omega_img = Image.fromarray(np.uint8(omega_img))


    delta_img_all.append(delta_img)
    theta_img_all.append(theta_img)
    omega_img_all.append(omega_img)




fig, axes = plt.subplots(3, 4, sharex=False, figsize=(9,6))

cmap = "gnuplot"

img11 = axes[0][0].imshow(delta_img_all[0],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img12 = axes[0][1].imshow(delta_img_all[1],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img13 = axes[0][2].imshow(delta_img_all[2],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img14 = axes[0][3].imshow(delta_img_all[3],  cmap=cmap, interpolation=None, vmin=0, vmax=255)

img21 = axes[1][0].imshow(theta_img_all[0],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img22 = axes[1][1].imshow(theta_img_all[1],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img23 = axes[1][2].imshow(theta_img_all[2],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img24 = axes[1][3].imshow(theta_img_all[3],  cmap=cmap, interpolation=None, vmin=0, vmax=255)

img31 = axes[2][0].imshow(omega_img_all[0],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img32 = axes[2][1].imshow(omega_img_all[1],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img33 = axes[2][2].imshow(omega_img_all[2],  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img34 = axes[2][3].imshow(omega_img_all[3],  cmap=cmap, interpolation=None, vmin=0, vmax=255)

for rows in axes:
    for ax in rows:
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.set_yticks([])
        ax.set_xticks([])
        # ax.set_yticks((0, 180))
        # ax.set_xticks((0, 180))
        # ax.yaxis.set_minor_locator(MultipleLocator(90))
        # ax.yaxis.set_ticklabels([r"", ""], fontsize=12)
        # ax.xaxis.set_minor_locator(MultipleLocator(90))
        # ax.xaxis.set_ticklabels(["", r""])



for rows in axes:
    rows[0].set_yticks((0, 180))
    rows[0].yaxis.set_minor_locator(MultipleLocator(90))
    rows[0].yaxis.set_ticklabels([r"$\pi$", "0"], fontsize=12)
    rows[0].set_ylabel(r"$\omega$", fontsize=12)

for ax in axes[2]:
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=12)
    ax.set_xlabel(r"$\delta$, 6$\theta$", fontsize=12)
    ax.set_xticks((0, 180))
    ax.xaxis.set_minor_locator(MultipleLocator(90))
    ax.xaxis.set_ticklabels(["0", r"$\pi$"], fontsize=12)

i = 1
for rows in axes:
    # divider = make_axes_locatable(ax)
    # cax = divider.append_axes('right', size='8%', pad=0.05)
    ax = rows[3]
    cax = fig.add_axes([ax.get_position().x1 + 0.01, ax.get_position().y0, 0.02, ax.get_position().height])
    # if i == 1:
    #     cbar = fig.colorbar(img11, cax=cax, orientation='vertical', ticks=[0, 127, 255], fraction=0.2)
    #     cbar.set_label(r"$1-\frac{\lg\Delta_{\delta}}{\lg\epsilon}$", fontsize=14)
    # elif i == 2:
    #     cbar = fig.colorbar(img21, cax=cax, orientation='vertical', ticks=[0, 127, 255])
    #     cbar.set_label(r"$1-\frac{\lg\Delta_{\theta}}{\lg\epsilon}$", fontsize=14)
    # elif i == 3:
    #     cbar = fig.colorbar(img31, cax=cax, orientation='vertical', ticks=[0, 127, 255])
    #     cbar.set_label(r"$1-\frac{\lg\Delta_{\omega}}{\lg\epsilon}$", fontsize=14)
    if i == 1:
        cbar = fig.colorbar(img11, cax=cax, orientation='vertical', ticks=[0, 127, 255])
        cbar.set_label(r"$\Delta D_\delta$", fontsize=12)
    elif i == 2:
        cbar = fig.colorbar(img21, cax=cax, orientation='vertical', ticks=[0, 127, 255])
        cbar.set_label(r"$\Delta D_\omega$", fontsize=12)
    elif i == 3:
        cbar = fig.colorbar(img31, cax=cax, orientation='vertical', ticks=[0, 127, 255])
        cbar.set_label(r"$\Delta D_\epsilon$", fontsize=12)

    cbar.ax.invert_yaxis()
    cbar.ax.set_yticklabels(['1<', '0.5', '0'], fontsize=12)

    i = i + 1

#plt.subplots_adjust(wspace=0.05, hspace=0.05)

plt.subplots_adjust(wspace=0.1, hspace=0.1)
plt.savefig(f'S_Fig1.tiff', format='tiff', dpi=1000, bbox_inches='tight')

plt.show()



