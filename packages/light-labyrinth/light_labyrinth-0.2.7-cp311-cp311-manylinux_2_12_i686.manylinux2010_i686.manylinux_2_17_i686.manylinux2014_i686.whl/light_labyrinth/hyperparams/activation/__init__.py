"""
The `light_labyrinth.hyperparams.activation` module includes `ReflectiveIndex` classes
with predefined splitting criteria (or activation functions) that can be used for building Light Labyrinth models. 
"""

from ._activation2d import ReflectiveIndexCalculator, ReflectiveIndexCalculatorRandom
from ._activation3d import ReflectiveIndexCalculator3D, ReflectiveIndexCalculator3DRandom

__all__ = ["ReflectiveIndexCalculator", "ReflectiveIndexCalculatorRandom",
           "ReflectiveIndexCalculator3D", "ReflectiveIndexCalculator3DRandom"]