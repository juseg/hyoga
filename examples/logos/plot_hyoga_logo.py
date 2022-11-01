#!/usr/bin/env python
# Copyright (c) 2021-2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
Hyoga logo
==========

Plot hyoga logo and favicon and including glaciers and paleoglaciers.
"""

import matplotlib.pyplot as plt
import hyoga


def get_height_dots(fig):
    """Return the figure height in dots."""
    return fig.get_window_extent().height/fig.dpi*72


def plot_favicon(figsize=None, rect=None, color='0.25'):
    """Plot main part of the logo."""

    # initialize figure
    fig = plt.figure(figsize=(9.6, 9.6) if figsize is None else figsize)
    ax = fig.add_axes([3/32, 5/128, 13/16, 13/16] if rect is None else rect)

    # add continents and glaciers
    crs = '+a=6378137 +proj=ortho +lon_0=-45 +lat_0=90'
    hyoga.open.natural_earth(
        'admin_0_countries', category='cultural', scale='110m')\
        .to_crs(crs).plot(ax=ax, alpha=0.25, facecolor=color)
    hyoga.open.paleoglaciers('ehl11').to_crs(crs).plot(
        ax=ax, alpha=0.75, facecolor=color)
    hyoga.open.natural_earth('glaciated_areas', scale='50m').to_crs(crs).plot(
        ax=ax, edgecolor=color, facecolor=color)

    # add circle for the o
    ax.add_patch(plt.Circle(
        (0, 0), 6.4e6, capstyle='round', clip_on=False, edgecolor=color,
        facecolor='none', linewidth=5/64*get_height_dots(fig)))

    # add overline (in default fig coords this is [1/4, 3/4], 15/16, 1)
    ax.fill_between(
        [5/26, 21/26], 115/104, 123/104, clip_on=False, facecolor=color,
        transform=ax.transAxes)

    # set axes properties
    ax.patch.set_facecolor('none')
    ax.set_xlim((-6.4e6, 6.4e6))
    ax.set_ylim((-6.4e6, 6.4e6))
    ax.axis('off')

    # return figure
    return fig


def plot_logo(color='0.25'):
    """Plot full logo with text."""

    # plot favicon with wide layout
    fig = plot_favicon(
        figsize=(9.6, 3.2), rect=[17/48, 5/128, 14/48, 13/16], color=color)

    # add text and overline
    fig.text(
        1/2, 0, 'hy  ga', color=color, family='monospace', ha='center',
        va='bottom', fontsize=7/8*get_height_dots(fig))

    # return figure
    return fig


# %%
# Full logo with package name
plot_logo()
plt.show()

# %%
# Small logo for the favicon
plot_favicon()
plt.show()
