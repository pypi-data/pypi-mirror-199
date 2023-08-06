from enum import Enum


class ErrorCalculator(Enum):
    """
    ErrorCalculator class includes all the available error functions
    for Light Labyrinth models.

    Error function is the function that for an array of model's weights \\(W\\) and an input vector \\(x\\)
    computes how much the predicted output \\(\\hat{y}\\) differs from the target values \\(y\\).
    The goal of the learning process is finding a minimum of this function. It is done by performing
    series of adjustements to model's weights which requires finding its gradient.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.error_function import ErrorCalculator
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             error=ErrorCalculator.cross_entropy)
    """
    mean_squared_error = 1
    """
    Mean squared error (MSE). It can be used for any type of classification and regression problem.
    \\[MSE(\\mathbf{y}, \\mathbf{\\hat{y}}) =  \\frac{1}{k}\\displaystyle\\sum_{i=1}^{k} (y_i-\\hat{y_i})^2\\]
    """
    cross_entropy = 2
    """
    Cross entropy loss (CE). Primarily for classification tasks, however due to Light Labyrinth's structure it 
    can be used for regression as well.
    \\[CE(\\mathbf{y}, \\mathbf{\\hat{y}}) =  -\\displaystyle\\sum_{i=1}^{k} y_i log(\\hat{y_i})\\]
    """
    scaled_mean_squared_error = 3
    """
    Scaled mean squared error (SMSE). Adaptation of MSE meant primarily for multi-label classification.
    Output values of consecutive pairs of output nodes are scaled to add up to \\(\\frac{1}{k}\\), where \\(k\\) is the number of distinct classes.
    \\[SMSE(\\mathbf{y}, \\mathbf{\\hat{y}}) = \\frac{1}{k} \\displaystyle\\sum_{i=0}^{k-1} \\left(\\left(\\frac{\\hat{y}_{2i}}{(\\hat{y}_{2i} + \\hat{y}_{2i+1})k} - y_{2i}\\right)^2 + \\left(\\frac{\\hat{y}_{2i+1}}{(\\hat{y}_{2i} + \\hat{y}_{2i+1})k} - y_{2i+1}\\right)^2\\right)\\]

    """
