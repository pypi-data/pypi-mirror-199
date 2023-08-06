from enum import Enum


class ReflectiveIndexCalculator3D(Enum):
    """
    ReflectiveIndexCalculator3D class includes all the available splitting criteria 
    for 3-dimensional Light Labyrinth models.

    Splitting criterion in a LightLabyrinth3D model is the function that for a given node \\(W_{ij}^t\\) and an input vector \\(x\\)
    outputs the portion of light reflected in all three directions - to the left \\(p_{ij}^{tL}\\), right \(p_{ij}^{tR}\\) and up \(p_{ij}^{tU}\\). These three values always
    add up to 1.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.activation import ReflectiveIndexCalculator3D
    >>> from light_labyrinth.dim3 import LightLabyrinth3DClassifier
    >>> model = LightLabyrinthClassifier(3, 3, 2,
    ...                             activation=ReflectiveIndexCalculator3D.softmax_dotproduct_3d)
    """
    softmax_dotproduct_3d = 1
    """
    The portion of light reflected in all three directions is given by the softmax function over
    product of the input vector \\(x\\) and the matrix of weights \\(W_{ij}^t\\).
    \\[SD3d(x, W_{ij}^t) =  \\sigma(x \cdot W_{ij}^t) = \\sigma\\Big(\\begin{bmatrix} p_{ij}^{tL} & p_{ij}^{tR} & p_{ij}^{tU} \\end{bmatrix}^T\\Big) \\\\
    \\sigma(v)_i = \\frac{e^{v_i}}{\\sum_{j=1}^Z e^{v_j}} \\text{ for } i \\in \\{1,...,Z\\}\\]
    """


class ReflectiveIndexCalculator3DRandom(Enum):
    """
    ReflectiveIndexCalculator3DRandom class includes all the available splitting criteria 
    for 3-dimensional random Light Labyrinth models.

    Splitting criterion in a LightLabyrinth3DRandom model is the function that for a given node \\(W_{ij}^t\\), a subset of indices \\(B_{ij}^t\\) and an input vector \\(x\\)
    outputs the portion of light reflected in all three directions - to the left \\(p_{ij}^{tL}\\), right \(p_{ij}^{tR}\\) and up \(p_{ij}^{tU}\\). These three values always
    add up to 1.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.activation import ReflectiveIndexCalculator3DRandom
    >>> from light_labyrinth.dim3 import LightLabyrinth3DRandomClassifier
    >>> model = LightLabyrinth3DRandomClassifier(3, 3, 2, features=0.7,
    ...                             activation=ReflectiveIndexCalculator3DRandom.random_3d_softmax_dotproduct)
    """
    random_3d_softmax_dotproduct = 1
    """
    The portion of light reflected in all three directions is given by the softmax function over
    product of the input vector \\(x\\) and the matrix of weights \\(W_{ij}^t\\) masked
    by the binary matrix holding relevant indices \\(B_{ij}^t\\).
    \\[RSD3d(x, W_{ij}^t, B_{ij}^t) =  \\sigma(x \cdot (W_{ij}^t * B_{ij}^t)) = \\sigma\\Big(\\begin{bmatrix} p_{ij}^{tL} & p_{ij}^{tR} & p_{ij}^{tU} \\end{bmatrix}^T\\Big) \\\\
    \\sigma(v)_i = \\frac{e^{v_i}}{\\sum_{j=1}^Z e^{v_j}} \\text{ for } i \\in \\{1,...,Z\\}\\]
    """
