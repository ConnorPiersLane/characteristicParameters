import math
import os
import pickle

import numpy as np
from matplotlib import pyplot as plt
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.axes_grid1 import make_axes_locatable

with open(os.path.join('fig4_std_errors.pickle'), 'rb') as handle:
    std_errors = pickle.load(handle)

rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]


Z1 = std_errors[0]
Z2 = std_errors[1]
Z3 = std_errors[2]

Z2 = [math.degrees(x) for x in y for y ]


# Chose a fixed theta
theta = math.radians(125)
theta_expected = theta % math.pi/2

# Error analyis
# N times the corresponding characteristic parameters are calculated
N = 1000
error_std = 1e-3  # mean and standard deviation

# Settings
stepsize = math.radians(1)

# y-axis
omegas = np.arange(0, math.pi + stepsize / 2, stepsize)
Y = omegas
# x-axis
deltas = np.arange(0, 4 * math.pi + stepsize / 2, stepsize)
X = deltas

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, sharex=False, constrained_layout=True)

cmap = "inferno_r"
# cmap = ListedColormap([ "whitesmoke", "grey", "black", "red"])
levels1 = [0.0, 0.005, 0.01, 0.015, 0.02, 0.025, 0.03]
CS1 = ax1.contourf(X, Y, Z1, cmap="viridis_r", levels=levels1,)
levels2 = [0.0, 0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5]
CS2 = ax2.contourf(X, Y, Z2, cmap=cmap,levels=levels2,)
CS3 = ax3.contourf(X, Y, Z3, cmap=cmap,levels=levels2, extend="max")

i = 1
for ax in (ax1, ax2, ax3):

    ax.set_yticks((0, math.pi))
    ax.yaxis.set_minor_locator(MultipleLocator(math.pi/2))
    ax.yaxis.set_ticklabels(["0", r"$\pi$"], fontsize=12)

    ax.set_ylabel(r"$\omega$", fontsize=12)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=12)

    ax.set_xticks((0, math.pi, 2*math.pi, 3*math.pi, 4*math.pi))
    ax.xaxis.set_minor_locator(MultipleLocator(math.pi/2))
    ax.xaxis.set_ticklabels(["0", r"$\pi$", r"$2\pi$", r"$3\pi$", r"$4\pi$"])

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)

    divider = make_axes_locatable(ax)
    cax = divider.append_axes('right', size='3%', pad=0.1)

    if i == 1:

        cbar = fig.colorbar(CS1, cax=cax, orientation='vertical', ticks=[0, 0.01, 0.02, 0.03])
        cbar.set_label(r"$\Delta \delta$", fontsize=12)
        ax.text(-0.12, 1.1, "(a)", transform=ax.transAxes,
                size=12, weight='bold')
    elif i == 2:
        cbar = fig.colorbar(CS2, cax=cax, orientation='vertical', ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5])
        cbar.set_label(r"$\Delta \theta$", fontsize=12)
        ax.text(-0.12, 1.1, "(b)", transform=ax.transAxes,
                size=12, weight='bold')
    elif i == 3:
        cbar = fig.colorbar(CS3, cax=cax, orientation='vertical', ticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], extend="max")
        cbar.set_label(r"$\Delta \omega$", fontsize=12)
        ax.text(-0.12, 1.1, "(c)", transform=ax.transAxes,
                size=12, weight='bold')



    i = i + 1

ax3.set_xlabel(r"$\delta$", fontsize=12)

plt.savefig('Fig4.tiff', format='tiff', dpi=2000, bbox_inches='tight')
plt.show()
