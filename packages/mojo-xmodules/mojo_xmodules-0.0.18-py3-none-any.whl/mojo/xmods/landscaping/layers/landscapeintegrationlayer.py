"""
.. module:: landscapeintegrationlayer
    :platform: Darwin, Linux, Unix, Windows
    :synopsis: Module containing the :class:`LandscapeItegrationLayer` class which is used
               to load initialize the test landscape and integrate with all the available
               landscape resources.

.. moduleauthor:: Myron Walker <myron.walker@gmail.com>

"""

__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

from typing import TYPE_CHECKING

from mojo.xmods.landscaping.layers.landscapinglayerbase import LandscapingLayerBase

if TYPE_CHECKING:
    from mojo.xmods.landscaping.landscape import Landscape


class LandscapeIntegrationLayer(LandscapingLayerBase):

    def __init__(self, lscape: "Landscape"):
        super().__init__(lscape)
        return
    
    def topology_overlay(self) -> None:
        return
