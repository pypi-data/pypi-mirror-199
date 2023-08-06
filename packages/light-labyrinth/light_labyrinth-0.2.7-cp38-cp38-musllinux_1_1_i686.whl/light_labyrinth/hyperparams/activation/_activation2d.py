from enum import Enum


class ReflectiveIndexCalculator(Enum):
    """
    ReflectiveIndexCalculator class includes all the available splitting criteria 
    for 2-dimensional Light Labyrinth models.

    Splitting criterion in a LightLabyrinth model is the function that for a given node \\(W_{ij}\\) and an input vector \\(x\\)
    outputs the portion of light reflected \\(p_{ij}^L\\) and passed through \\(p_{ij}^R\\). These two values always
    add up to 1.


    Examples
    --------
    >>> from light_labyrinth.hyperparams.activation import ReflectiveIndexCalculator
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             activation=ReflectiveIndexCalculator.sigmoid_dot_product)
    """
    sigmoid_dot_product = 1
    """
    The portion of light reflected is given by the logistic function over dot product of the input vector \\(x\\) and vector of weights \\(W_{ij}\\).
    \\[SD(x, W_{ij}) = \\begin{bmatrix} f(x \cdot W_{ij}) \\\\ 1 - f(x \cdot W_{ij}) \\end{bmatrix} = \\begin{bmatrix} p_{ij}^L \\\\ p_{ij}^R \\end{bmatrix} \\\\
    f(v) = \\frac{1}{1+e^{-v}}\\]
    """


class ReflectiveIndexCalculatorRandom(Enum):
    """
    ReflectiveIndexCalculatorRandom class includes all the available splitting criteria 
    for 2-dimensional random Light Labyrinth models.

    Splitting criterion in a LightLabyrinthRandom model is the function that for a given 
    node \\(W_{ij}\\), a subset of indices \\(B_{ij}\\) and an input vector \\(x\\) outputs
    the portion of light reflected \\(p_{ij}^L\\) and passed through \\(p_{ij}^R\\). 
    These two values always add up to 1.    

    Examples
    --------
    >>> from light_labyrinth.hyperparams.activation import ReflectiveIndexCalculatorRandom
    >>> from light_labyrinth.dim2 import LightLabyrinthRandomRegressor
    >>> model = LightLabyrinthRandomRegressor(4, 3, features=0.6,
    ...                             activation=ReflectiveIndexCalculatorRandom.random_sigmoid_dot_product)
    """
    random_sigmoid_dot_product = 1
    """
    The portion of light reflected is given by the logistic function over dot product of the input vector \\(x\\) and vector of weights \\(W_{ij}\\) masked
    by the binary vector holding relevant indices \\(B_{ij}\\).
    \\[RSD(x, W_{ij}, B_{ij}) = \\begin{bmatrix} f(x \cdot (W_{ij}*B_{ij})) \\\\ 1 - f(x \cdot (W_{ij}*B_{ij})) \\end{bmatrix} = \\begin{bmatrix} p_{ij}^L \\\\ p_{ij}^R \\end{bmatrix} \\\\
    f(v) = \\frac{1}{1+e^{-v}}\\]
    """
