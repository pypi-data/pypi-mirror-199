"""
The `light_labyrinth.dim3` module includes 3-dimensional Light Labyrinth models.

.. include:: ../../html_utils/3dclassifier.svg
"""

from ._LightLabyrinth3DClassifier import LightLabyrinth3DClassifier
from ._LightLabyrinth3DRandomClassifier import LightLabyrinth3DRandomClassifier

__all__ = ["LightLabyrinth3DClassifier", "LightLabyrinth3DRandomClassifier"]