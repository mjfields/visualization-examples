"""
An example of how to make a corner plot using Seaborn.
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

### generate random data ###
rng = np.random.default_rng(seed=1234)

data = rng.normal(0.5, 0.1, size=(5, 1000))
data_df = pd.DataFrame(data.T, columns=['a', 'b', 'c', 'd', 'e'])

### make the plot ###
## initialize a PairGrid with the data we generated
grid = sns.PairGrid(data_df, corner=True, diag_sharey=False)

## draw the shaded 2D contours
grid.map_offdiag(
    sns.kdeplot,
    fill=True,
    color='cornflowerblue',
    levels=4,
    cut=0,
    bw_adjust=2
)
## draw the contour outlines
grid.map_offdiag(
    sns.kdeplot,
    fill=False,
    color='black',
    levels=4,
    linewidths=3,
    cut=0,
    bw_adjust=2
)
## draw the 1D distributions at the diagonal
grid.map_diag(
    sns.kdeplot,
    fill=True,
    color='cornflowerblue',
    edgecolor='black',
    linewidth=3,
    cut=0,
    bw_adjust=2,
    alpha=0.7
)

## write the titles that go above the diagonals
for label, chain, diag_ax in zip(data_df.columns, data_df.T.values, grid.diag_axes):
    p = np.percentile(chain, [16, 50, 84])
    q = np.diff(p)
    diag_ax.set_title(
        fr"${label.replace('$', '')} = {p[1]:{'.2f'}}_{{-{q[0]:{'.2f'}}}}^{{+{q[1]:{'.2f'}}}}$",
        fontsize=16
    )

plt.savefig("corner.png")

plt.show()