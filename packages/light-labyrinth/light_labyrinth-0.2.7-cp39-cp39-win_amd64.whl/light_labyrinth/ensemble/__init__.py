"""
The `light_labyrinth.ensemble` module includes ensemble models
built of random Light Labyrinth estimators. Such ensemble is referred to 
as `Random Maze`.
"""

from ._RandomMaze2DClassifier import RandomMaze2DClassifier
from ._RandomMaze3DClassifier import RandomMaze3DClassifier

from ._RandomMazeRegressor import RandomMazeRegressor

__all__ = ["RandomMaze2DClassifier", "RandomMaze3DClassifier", "RandomMazeRegressor"]