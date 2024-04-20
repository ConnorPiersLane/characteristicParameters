import math
import os.path
import pickle
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from matplotlib.colors import ListedColormap
from mpl_toolkits.axes_grid1 import make_axes_locatable

from characteristicParameters.triangle_wave_functions import T_pi
from matplotlib.ticker import MultipleLocator


rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]

with open(os.path.join('data','fig4_measured_values.pickle'), 'rb') as handle:
    measured_values = pickle.load(handle)

with open(os.path.join('data','fig4_true_values.pickle'), 'rb') as handle:
    true_values = pickle.load(handle)


ncol = 181  # because stepsize was 1° including omega=0° and omega=180°

delta_true = []
theta_true = []
omega_true = []

delta_tilde = []
theta_tilde = []
omega_tilde = []

for (measured_value, true_value) in zip(measured_values, true_values):

    delta_limit = 4*math.pi

    if not math.isclose(true_value[0], delta_limit) and true_value[0] > delta_limit:
        continue

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

delta_diff = [i if i < 1 else 1 for i in delta_diff]
theta_diff = [i if i < 1 else 1 for i in theta_diff]
omega_diff = [i if i < 1 else 1 for i in omega_diff]



delta_diff_log = list(- np.log10(delta_diff))
theta_diff_log = list(- np.log10(theta_diff))
omega_diff_log = list(- np.log10(omega_diff))

eps = np.finfo(float).eps

delta_diff_log = list(np.log10(delta_diff)/np.log10(eps))
theta_diff_log = list(np.log10(theta_diff)/np.log10(eps))
omega_diff_log = list(np.log10(omega_diff)/np.log10(eps))



delta_diff_log_s = [i*255 if i < 1 else 255 for i in delta_diff_log]
theta_diff_log_s = [i*255 if i < 1 else 255 for i in theta_diff_log]
omega_diff_log_s = [i*255 if i < 1 else 255 for i in omega_diff_log]


# Change the arrays into an image
delta_img = np.flipud(np.reshape(delta_diff_log_s, (-1, ncol)).T)
theta_img = np.flipud(np.reshape(theta_diff_log_s, (-1, ncol)).T)
omega_img = np.flipud(np.reshape(omega_diff_log_s, (-1, ncol)).T)

delta_img = Image.fromarray(np.uint8(delta_img))
theta_img = Image.fromarray(np.uint8(theta_img))
omega_img = Image.fromarray(np.uint8(omega_img))

fig, (ax1, ax2, ax3) = plt.subplots(3,1, sharex=False, constrained_layout=True)

cmap = "inferno"
#cmap = ListedColormap([ "whitesmoke", "grey", "black", "red"])
img1 = ax1.imshow(delta_img,  cmap=cmap, interpolation=None, vmin=0, vmax=255)
img2 = ax2.imshow(theta_img, cmap=cmap, interpolation=None, vmin=0, vmax=255)
img3 = ax3.imshow(omega_img, cmap=cmap, interpolation=None, vmin=0, vmax=255)

i = 1

for ax in (ax1, ax2, ax3):

    ax.set_yticks((0, 180))
    ax.yaxis.set_minor_locator(MultipleLocator(90))
    ax.yaxis.set_ticklabels([r"$\pi$", "0"], fontsize=12)

    ax.set_ylabel(r"$\omega$", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=12)


    ax.set_xticks((0, 180, 360, 540, 720))
    ax.xaxis.set_minor_locator(MultipleLocator(90))
    ax.xaxis.set_ticklabels(["0", r"$\pi$", r"$2\pi$", r"$3\pi$", r"$4\pi$"])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)


    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='3%', pad=0.1)


    # if i == 1:
    #     cbar = fig.colorbar(img1, cax=cax, orientation='vertical', ticks=[0, 127, 255])
    #     cbar.set_label(r"$1-\frac{\lg\Delta_{\delta}}{\lg\epsilon}$", fontsize=14)
    # elif i == 2:
    #     cbar = fig.colorbar(img2, cax=cax, orientation='vertical', ticks=[0, 127, 255])
    #     cbar.set_label(r"$1-\frac{\lg\Delta_{\theta}}{\lg\epsilon}$", fontsize=14)
    # elif i == 3:
    #     cbar = fig.colorbar(img3, cax=cax, orientation='vertical', ticks=[0, 127, 255])
    #     cbar.set_label(r"$1-\frac{\lg\Delta_{\omega}}{\lg\epsilon}$", fontsize=14)

    if i == 1:
        cbar = fig.colorbar(img1, cax=cax, orientation='vertical', ticks=[0, 127, 255], extend="min")
        cbar.set_label(r"$\Delta D_\delta$", fontsize=12)
        ax.text(-0.12, 1.1, "(a)", transform=ax.transAxes,
                size=12,weight='bold')
    elif i == 2:
        cbar = fig.colorbar(img2, cax=cax, orientation='vertical', ticks=[0, 127, 255], extend="min")
        cbar.set_label(r"$\Delta D_\theta$", fontsize=12)
        ax.text(-0.12, 1.1, "(b)", transform=ax.transAxes,
                size=12,weight='bold')
    elif i == 3:
        cbar = fig.colorbar(img3, cax=cax, orientation='vertical', ticks=[0, 127, 255], extend="min")
        cbar.set_label(r"$\Delta D_\omega$", fontsize=12)
        ax.text(-0.12, 1.1, "(c)", transform=ax.transAxes,
                size=12,weight='bold')

    cbar.ax.invert_yaxis()
    cbar.ax.set_yticklabels(['1', '0.5', '0'])

    i = i + 1


ax3.set_xlabel(r"$\delta$, 6$\theta$", fontsize=12)
# fig.tight_layout()
plt.savefig('Fig4_v2.tiff', format='tiff', dpi=2000, bbox_inches='tight')

plt.show()



