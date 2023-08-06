from enum import Enum


class LightLabyrinthWeightsInit(Enum):
    """
    This class allows to initialize Light Labyrinth model's weights either
    with zeros or randomly.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.weights_init import LightLabyrinthWeightsInit
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             weights_init=LightLabyrinthWeightsInit.Random)
    """
    Default = 0
    """
    """
    Random = 1
    """
    Initializes model's weights randomly -- initial weights are drawn from the uniform distribution [-1,1].
    """
    Zeros = 2
    """
    Initializes model's weights with zeros.
    """
