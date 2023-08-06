class _RegularizationBase:
    def __init__(self, name, options):
        self._name = name
        self._options = options

    @property
    def name(self):
        return self._name

    @property
    def options(self):
        return self._options


class RegularizationNone(_RegularizationBase):
    """
    None regularization -- to be used when no regularization is needed.

    See Also
    --------
    light_labyrinth.hyperparams.regularization.RegularizationL1 : L1 regularization
    light_labyrinth.hyperparams.regularization.RegularizationL2 : L2 regularization

    Examples
    --------
    >>> from light_labyrinth.hyperparams.regularization import RegularizationNone
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             regularization=RegularizationNone())
    """

    def __init__(self):
        super().__init__("None", [])


class RegularizationL1(_RegularizationBase):
    """
    L1 regularization -- at each iteration of the learning process a sum
    of the absoute values (first norm) of model's weights is added to the 
    error function. This stops the weights from getting too big or too
    small and in effect prevents (to some extent) overfitting.

    The optimized error function with L1 regularization can we written as
    \\[\\xi(W, X, y) =  \\lambda |W| + \sum_{i=0}^{n-1} \sum_{j=0}^{k-1} err(y_{ij}, \hat{y}_{ij})\\]
    where \\(\\lambda>0\\) is a regularization factor. 

    Parameters
    ----------
    ----------
    lambda_factor : float, default=0.01
        The regularization factor which controls the importance of regularization.
        The higher it is, the less the model will overfit. Note however that too high
        regularization factor may prevent model from fitting at all.

    Attributes
    ----------
    ----------
    learning_rate : float
        The regularization factor.

    See Also
    --------
    light_labyrinth.hyperparams.regularization.RegularizationNone : No regularization
    light_labyrinth.hyperparams.regularization.RegularizationL2 : L2 regularization

    Examples
    --------
    >>> from light_labyrinth.hyperparams.regularization import RegularizationL1
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             regularization=RegularizationL1(0.001))
    """

    def __init__(self, lambda_factor=0.01):
        super().__init__("L1", [lambda_factor])
        self._lambda_factor = lambda_factor

    @property
    def lambda_factor(self):
        self._lambda_factor


class RegularizationL2(_RegularizationBase):
    """
    L2 regularization -- at each iteration of the learning process a sum
    of squared values (second norm) of model's weights is added to the 
    error function. This stops the weights from getting too big or too
    small and in effect prevents (to some extent) overfitting.

    The optimized error function with L2 regularization can we written as
    \\[\\xi(W, X, y) =  \\frac{\\lambda}{2} ||W|| + \sum_{i=0}^{n-1} \sum_{j=0}^{k-1} err(y_{ij}, \hat{y}_{ij})\\]
    where \\(\\lambda>0\\) is a regularization factor. 

    Parameters
    ----------
    ----------
    lambda_factor : float, default=0.01
        The regularization factor which controls the importance of regularization.
        The higher it is, the less the model will overfit. Note however that too high
        regularization factor may prevent model from fitting at all.

    Attributes
    ----------
    ----------
    learning_rate : float
        The regularization factor.

    See Also
    --------
    light_labyrinth.hyperparams.regularization.RegularizationNone : No regularization
    light_labyrinth.hyperparams.regularization.RegularizationL1 : L1 regularization

    Examples
    --------
    >>> from light_labyrinth.hyperparams.regularization import RegularizationL2
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             regularization=RegularizationL2(0.001))
    """

    def __init__(self, lambda_factor=0.01):
        super().__init__("L2", [lambda_factor])
        self._lambda_factor = lambda_factor

    @property
    def lambda_factor(self):
        self._lambda_factor
