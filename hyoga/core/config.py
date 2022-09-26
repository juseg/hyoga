# Copyright (c) 2022, Julien Seguinot (juseg.github.io)
# GNU General Public License v3.0+ (https://www.gnu.org/licenses/gpl-3.0.txt)

"""
This module contains configuration parameters used by Hyoga interpolation and
plot methods. There is currently only one configuration parameter.
"""

from dataclasses import dataclass


@dataclass
class HyogaConfig:
    """Hyoga configuration parameters.

    Parameters
    ----------
    glacier_masking_point : float, optional (default 1.0)
        Thickness threshold used to consider grid cells as glacierized.
    """
    glacier_masking_point: float = 1.0

    def __setattr__(self, name, value):
        """Check attribute validity before setting value."""
        if hasattr(self, name):
            object.__setattr__(self, name, value)
        else:
            raise TypeError(f'{name} is not a valid configuration parameter')


config = HyogaConfig()
