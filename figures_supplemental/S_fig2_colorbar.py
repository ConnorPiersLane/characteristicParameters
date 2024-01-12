# https://matplotlib.org/3.1.0/tutorials/colors/colorbar_only.html


from matplotlib import pyplot as plt
import matplotlib as mpl
from matplotlib.colors import ListedColormap
rc = {"font.family": "serif",
      "mathtext.fontset": "stix"}
plt.rcParams.update(rc)
plt.rcParams["font.serif"] = ["Times New Roman"] + plt.rcParams["font.serif"]




fig, ax = plt.subplots(figsize=(3, 1))
fig.subplots_adjust(bottom=0.6)

cmap = ListedColormap(['whitesmoke', "grey", "black", 'red'])

cmap.set_over('red')
cmap.set_under('whitesmoke')

bounds = [-0.6, -0.5, 0.0, 0.5, 0.6]
norm = mpl.colors.BoundaryNorm(bounds, cmap.N)
cb3 = mpl.colorbar.ColorbarBase(ax, cmap=cmap,
                                norm=norm,
                                boundaries=bounds,
                                extend='both',
                                #extendfrac='auto',
                                #ticks=bounds,
                                #spacing='proportional',
                                orientation='horizontal',
                                )


cb3.ax.tick_params(size=0)
cb3.set_ticks(ticks=bounds, labels=["", "$10^{-13}$", "$10^{-9}$", "$10^{-5}$", ""], fontsize=12)
cb3.set_label(r"$\Delta_{\delta}$, $\Delta_{\theta}$, $\Delta_{\omega}$ [°]", fontsize=12)


fig.show()

plt.savefig('S_Fig2_colorbar.tiff', format='tiff', dpi=2000)
plt.show()