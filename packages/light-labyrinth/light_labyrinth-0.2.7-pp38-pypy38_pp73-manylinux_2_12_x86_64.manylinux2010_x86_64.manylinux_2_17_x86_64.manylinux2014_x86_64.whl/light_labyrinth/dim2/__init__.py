"""
The `light_labyrinth.dim2` module includes 2-dimensional Light Labyrinth models.
.. include:: ../../html_utils/2dclassifier.svg
"""

from ._LightLabyrinthClassifier import LightLabyrinthClassifier
from ._LightLabyrinthRegressor import LightLabyrinthRegressor

from ._LightLabyrinthDynamicClassifier import LightLabyrinthDynamicClassifier
from ._LightLabyrinthDynamicRegressor import LightLabyrinthDynamicRegressor

from ._LightLabyrinthRandomClassifier import LightLabyrinthRandomClassifier
from ._LightLabyrinthRandomRegressor import LightLabyrinthRandomRegressor

__all__ = ["LightLabyrinthClassifier", "LightLabyrinthRegressor", \
           "LightLabyrinthDynamicClassifier", "LightLabyrinthDynamicRegressor", \
           "LightLabyrinthRandomClassifier", "LightLabyrinthRandomRegressor"]