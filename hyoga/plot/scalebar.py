# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains a single class, which draws a horizontal scale bar with a
text label above it, inside a container, anchored to the matplotlib axes with a
fixed offset. This module may be renamed or merged with other axes decorations
in the future.
"""

import matplotlib as mpl


class AnchoredScaleBar(mpl.offsetbox.AnchoredOffsetbox):
    """Anchored horizontal scale bar with a text label above it."""
    # modified from the matplotlib 3.6 anchored artists example
    # https://matplotlib.org/stable/gallery/misc/anchored_artists.html

    def __init__(self, label, loc, size, transform, color=None, **kwargs):
        self.label = mpl.offsetbox.TextArea(label, textprops=dict(color=color))
        self.scale = mpl.offsetbox.AuxTransformBox(transform)
        self.scale.add_artist(mpl.lines.Line2D(
            [0, size], [0, 0], color=color, **kwargs))
        self._box = mpl.offsetbox.VPacker(
            children=[self.label, self.scale], align='center', pad=0, sep=0)
        super().__init__(loc, child=self._box, frameon=False)
