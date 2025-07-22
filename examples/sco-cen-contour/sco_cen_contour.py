"""
Generates a figure of position points for targets in
the Upper Scorpius OB association and Ophiuchus molecular cloud
on top of a 2D contour of nearby members of the Scorpius-Centaurus
OB association. Points are colored according to their median
disk-star alignment value. The figure contains an inset axis zooming
into the densest region of points. Sco-Cen target information is
downloaded with `astroquery`, and the Upper Sco and Ophiuchus target
information is within the 'target_info.txt' file.

The resulting figure is a reproduction of Fields et al. (in prep)
Figure 5.
"""

import sys
import os
sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            '..',
            '..',
            'common',
            'rcParams'
        )
    )
)
import custom_rcparams

import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.lines import Line2D

from astropy.coordinates import SkyCoord
import astropy.units as u
from astroquery.vizier import Vizier

### load the target position and alignment data ###
target_df = pd.read_csv("target_info.txt")
## transform to astropy coordinates
usco_coords = SkyCoord(
    *target_df[['ra', 'dec']].loc[target_df['region']=='usco'].values.T,
    unit=(u.degree, u.degree)
)
oph_coords = SkyCoord(
    *target_df[['ra', 'dec']].loc[target_df['region']=='oph'].values.T,
    unit=(u.degree, u.degree)
)

### download the sco-cen target data to make the contour ###
catalog = 'J/A+A/677/A59/tablee1'
vizier = Vizier(column_filters={'SigMA':'1 .. 9'})
vizier.ROW_LIMIT = -1
table = vizier.get_catalogs(catalog)[catalog]
## convert to dataframe
df = table[['_RA', '_DE']].to_pandas()

### make the figure ###
markersize = 18
lw = 1.75
alpha = 0.9
alpha_cmap = 'viridis'
norm = 'linear'
vmin, vmax = (10, 40)
umark = 'p'
omark = 'o'

fig, ax = plt.subplots(1, 1, figsize=(10, 10))

## plot the 2D contour
kws = dict(
    x=df['_RA'].values,
    y=df['_DE'].values,
    levels=7,
    alpha=0.7,
    ax=ax,
    zorder=-1
)
sco_cen_cmap = sns.color_palette("bone_r", as_cmap=True)
sns.kdeplot(fill=True, cmap=sco_cen_cmap, norm='log', **kws)
sns.kdeplot(fill=False, linewidths=2, colors='black', **kws)

## plot the points on top
## Upper Sco
sc = ax.scatter(
    usco_coords.ra.value,
    usco_coords.dec.value,
    s=markersize**2,
    c=target_df['alpha'].loc[target_df['region']=='usco'],
    marker=umark,
    cmap=alpha_cmap,
    norm=norm,
    vmin=vmin,
    vmax=vmax,
    linewidths=lw,
    edgecolors='black',
    alpha=alpha,
)
## Ophiuchus
ax.scatter(
    oph_coords.ra.value,
    oph_coords.dec.value,
    s=markersize**2,
    c=target_df['alpha'].loc[target_df['region']=='oph'],
    marker=omark,
    cmap=alpha_cmap,
    norm=norm,
    vmin=vmin,
    vmax=vmax,
    linewidths=lw,
    edgecolors='black',
    alpha=alpha,
)
cbar = fig.colorbar(
    sc,
    extend='both',
    pad=0.02,
    label=r"$\mid\alpha\mid$ ($^{\circ}$)"
)

ax.xaxis.set_inverted(True)
ax.set_xlim(268, 228)
ax.set_ylim(-43, -12)
xlim = ax.get_xlim()
ylim = ax.get_ylim()
ax.text(
    xlim[1] - 0.03*np.diff(xlim),
    ylim[1] - 0.03*np.diff(ylim),
    "Sco-Cen (Nearby)",
    verticalalignment='top',
    horizontalalignment='right',
    fontsize=22
)

## plot within an inset axis
axins_xlim = (247, 245.35)
axins_ylim = (-25.10, -23.10)
axins = ax.inset_axes(
    bounds=[255, -23, 20, 10],
    transform=ax.transData,
    xlim=axins_xlim,
    ylim=axins_ylim,
    xticklabels=[],
    yticklabels=[]
)
sns.kdeplot(fill=True, cmap=sco_cen_cmap, norm='log', **{**kws, **dict(ax=axins)})
sns.kdeplot(fill=False, linewidths=2, colors='black', **{**kws, **dict(ax=axins)})
axins.scatter(
    oph_coords.ra.value,
    oph_coords.dec.value,
    s=(markersize/1.1)**2,
    c=target_df['alpha'].loc[target_df['region']=='oph'],
    marker=omark,
    cmap=alpha_cmap,
    norm=norm,
    vmin=vmin,
    vmax=vmax,
    linewidths=lw/1.1,
    edgecolors='black',
    alpha=alpha,
    zorder=1000
)
axins.set_xlim(axins_xlim)
axins.set_ylim(axins_ylim)
axins.tick_params(axis='both', left=False, right=False, top=False, bottom=False)
for side in ['top','bottom','left','right']:
    axins.spines[side].set_linewidth(3)

## draw lines that point to the inset axis
ax.indicate_inset(
    bounds=[
        np.min(axins_xlim),
        np.min(axins_ylim),
        np.abs(np.diff(axins_xlim))[0],
        np.abs(np.diff(axins_ylim))[0]
    ],
    inset_ax=axins,
    transform=ax.transData,
    edgecolor="black", 
    linewidth=lw,
    alpha=0.7
)

ax2 = ax.twinx()
ax2.tick_params(axis='y', right=True, labelright=False, direction='in', zorder=-1)
ax2.spines['left'].set_visible(False)
ax2.set_ylim(ylim)

ax.set_xlabel(r"RA ($^{\circ}$)")
ax.set_ylabel(r"DEC ($^{\circ}$)")
ax.legend(
    handles=[
        Line2D(
            [],
            [],
            markersize=markersize,
            marker=umark,
            linestyle='',
            markerfacecolor='lightgray',
            markeredgecolor='black',
            markeredgewidth=lw,
            alpha=1,
            label="Upper Scorpius"
        ),
        Line2D(
            [],
            [],
            markersize=markersize,
            marker=omark,
            linestyle='',
            markerfacecolor='lightgray',
            markeredgecolor='black',
            markeredgewidth=lw,
            alpha=1,
            label="Ophiuchus"
        )
    ],
    loc='lower right',
)
plt.savefig("sco-cen_contour.png")
plt.show()