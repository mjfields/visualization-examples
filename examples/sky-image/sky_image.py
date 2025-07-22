"""
This script downloads and plots a real sky image in PS1 i-r-g 
color of a region within the Scorpius-Centaurus OB association.
The image is overlaid with marker points indicating targets
within the Upper Scorpius OB association and the Ophiuchus
molecular cloud. The target coordinates exist in 
'ra_dec_positions.txt'.

The resulting figure is a reproduction of Fields et al. (in prep)
Figure 1.
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
from matplotlib.lines import Line2D

from astropy.coordinates import SkyCoord
from astropy.coordinates import Longitude, Latitude, Angle
import astropy.units as u
from astropy.wcs import WCS
from astroquery.hips2fits import hips2fits

### download the sky image ###
hips = "CDS/P/PanSTARRS/DR1/color-i-r-g"
result = hips2fits.query(
   hips=hips,
   width=2100,
   height=1800,
   ra=Longitude(245.5055 * u.deg),
   dec=Latitude(-20 * u.deg),
   fov=Angle(15 * u.deg),
   projection="AIT",
   get_query_payload=False,
   format='fits',
   coordsys='icrs'
)
image = result[0].data
header = result[0].header
w = WCS(header)

### load the target positions ###
coord_df = pd.read_csv("ra_dec_positions.txt")
## transform them to astropy coordinates
usco_coords = SkyCoord(
    *coord_df[['ra', 'dec']].loc[coord_df['region']=='usco'].values.T,
    unit=(u.degree, u.degree)
)
oph_coords = SkyCoord(
    *coord_df[['ra', 'dec']].loc[coord_df['region']=='oph'].values.T,
    unit=(u.degree, u.degree)
)

### make the figure ###
markersize = 15

fig, ax = plt.subplots(1, 1, figsize=(10, 10))
ax.imshow(image.swapaxes(-2, -1).T, origin='lower')
## Upper Sco
ax.errorbar(
    *usco_coords.to_pixel(w),
    markersize=markersize,
    marker='p',
    linestyle='',
    markerfacecolor='cyan',
    markeredgecolor='white',
    alpha=0.3,
    zorder=1000
)
## Ophiuchus
ax.errorbar(
    *oph_coords.to_pixel(w),
    markersize=markersize,
    marker='o',
    linestyle='',
    markerfacecolor='magenta',
    markeredgecolor='white',
    alpha=0.3,
    zorder=1000
)

## convert pixels to degrees for axis ticks
xticks = np.arange(0, image.shape[2], image.shape[2] // 7)
yticks = np.arange(0, image.shape[1], image.shape[1] // 6)

crval = w.wcs.crval[:2]
crpix = w.wcs.crpix[:2]
cdelt = w.wcs.cdelt[:2]
low = crval - crpix*cdelt
high = crval + crpix*cdelt

ra_ticks = np.interp(xticks, np.arange(image.shape[2]), np.linspace(low[0], high[0], image.shape[2]))
ax.set_xticks(xticks)
ax.set_xticklabels([np.round(val, 1) for val in ra_ticks])
dec_ticks = np.interp(yticks, np.arange(image.shape[1]), np.linspace(low[1], high[1], image.shape[1]))
ax.set_yticks(yticks)
ax.set_yticklabels([np.round(val, 1) for val in dec_ticks])

ax.set_xlabel(r"RA ($^{\circ}$)")
ax.set_ylabel(r"DEC ($^{\circ}$)")

ax.legend(
    handles=[
        Line2D(
            [],
            [],
            markersize=markersize,
            marker='p',
            linestyle='',
            markerfacecolor='cyan',
            markeredgecolor='white',
            alpha=0.3,
            label="Upper Scorpius"
        ),
        Line2D(
            [],
            [],
            markersize=markersize,
            marker='o',
            linestyle='',
            markerfacecolor='magenta',
            markeredgecolor='white',
            alpha=0.3,
            # label=r"$\rho\,$Ophiuchus"
            label="Ophiuchus"
        )
    ],
    facecolor='black',
    labelcolor='lightgray',
    framealpha=0.3
)

plt.savefig("sky_image.png")

plt.show()