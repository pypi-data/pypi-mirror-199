class _OptimizerBase:
    def __init__(self, name, options):
        self._name = name
        self._options = options

    @property
    def name(self):
        return self._name

    @property
    def options(self):
        return self._options


class GradientDescent(_OptimizerBase):
    """
    Gradient Descent optimizer class for learning Light Labyrinth models.

    In each iteration \\(k\\) of the learning process, the loss function's gradient \\(\\nabla\\xi(W_{k}, X, y)\\) is computed, and the model's weights \\(W_k\\) are updated following the formulas:
    \\[\\Delta W_{k} = \\gamma \\Delta W_{k-1} + \\alpha \\nabla\\xi(W_{k}, X, y)\\\\
    W_{k+1} = W_{k} - \\Delta W_{k},\\]
    where \\(\\alpha\\) is a positive constant called the learning rate and \\(\\gamma \\in [0,1)\\) is a momentum coefficient.


    Parameters
    ----------
    ----------
    learning_rate : float, default=0.01
        The learning rate \\(\\alpha\\) -- a positive constant (usually not greater than 1.0) that controls the magnitude of steps taken in each iteration,
        and effectively the learning speed. Note that too high learning rate may lead to overshooting.

    momentum : float, default=0.0
        The momentum coefficient \\(\\gamma \\in [0,1) \\).

    Attributes
    ----------
    ----------
    learning_rate : float
        The learning rate.

    References
    ----------
    Sebastian Ruder
        "An overview of gradient descent optimization algorithms", CoRR (2016)
        <http://arxiv.org/abs/1609.04747>

    See Also
    --------
    light_labyrinth.hyperparams.optimization.Adam : Adam optimization algorithm.
    light_labyrinth.hyperparams.optimization.RMSprop : RMSprop optimization algorithm.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.optimization import GradientDescent
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             optimizer=GradientDescent(0.001, 0.9))
    """

    def __init__(self, learning_rate=0.01, momentum=0.0):
        super().__init__("Gradient_Descent", [learning_rate, momentum])
        self._learning_rate = learning_rate
        self._momentum = momentum

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def momentum(self):
        return self._momentum


class RMSprop(_OptimizerBase):
    """
    RMSprop optimizer class for learning Light Labyrinth models.

    In each iteration \\(k\\) of the learning process, the loss function's gradient \\(\\nabla\\xi(W_{k}, X, y)\\) is computed, and the model's weights \\(W_k\\) are updated following the formula:
    \\[v_{k} = \\rho v_{k-1}  + (1 - \\rho) (\\nabla\\xi(W_{k}, X, y))^2 \\\\
    \\Delta W_{k} = -\\gamma \\Delta W_{k-1} + \\frac{\\alpha}{\\sqrt{v_{k+1} + \\epsilon}}\\nabla\\xi(W_{k}, X, y) \\\\
    W_{k+1} = W_{k} - \\Delta W_{k}\\]
    Where \\(\\alpha>0\\) is the learning rate, \\(\\rho \\in (0,1)\\) is the forgetting factor, and \\(\\gamma \\in [0,1)\\) a momentum coefficient.
    The \\(\\epsilon>0\\) term ensures numerical stability and should not be too big. 


    Parameters
    ----------
    ----------
    learning_rate : float, default=0.01
        The learning rate \\(\\alpha\\) -- a positive constant (usually not greater than 1.0) that controls the magnitude of steps taken in each iteration,
        and effectively the learning speed. Note that too high learning rate may lead to overshooting.

    rho : float, default=0.9
        The forgetting factor \\(\\rho \\in (0,1)\\).

    momentum : float, default=0.0
        The momentum coefficient \\(\\gamma \\in [0,1)\\).

    epsilon : float, default=1e-6
        A smoothing term that avoids division by zero.

    Attributes
    ----------
    ----------
    learning_rate : float
        The learning rate.

    rho : float
        The forgetting factor.

    momentum : float
        The momentum coefficient.

    epsilon : float
        A smoothing term.

    References
    ----------
    ----------
    Sebastian Ruder
        "An overview of gradient descent optimization algorithms", CoRR (2016)
        <http://arxiv.org/abs/1609.04747>

    See Also
    --------
    light_labyrinth.hyperparams.optimization.Adam : Adam optimization algorithm.
    light_labyrinth.hyperparams.optimization.GradientDescent : GradientDescent optimization algorithm.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.optimization import RMSprop
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             optimizer=RMSprop(0.001))
    """

    def __init__(self, learning_rate=0.01, rho=0.9, momentum=0.0, epsilon=1e-6):
        super().__init__("RMSprop", [learning_rate, rho, momentum, epsilon])
        self._learning_rate = learning_rate
        self._rho = rho
        self._momentum = momentum
        self._epsilon = epsilon

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def rho(self):
        return self._rho

    @property
    def momentum(self):
        return self._momentum

    @property
    def epsilon(self):
        return self._epsilon


class Adam(_OptimizerBase):
    """
    Adam (Adaptive Moment Estimation) optimizer class for learning Light Labyrinth models.

    In each iteration \\(k\\) of the learning process, the loss function's gradient \\(\\nabla\\xi(W_{k}, X, y)\\) is computed, and the model's weights \\(W_k\\) are updated.
    Firstly the first \\(m_k\\) and the second \\(v_k\\) momentum of the gradient is computed
    \\[m_k = \\beta_1 m_{k-1} + (1-\\beta_1)\\nabla\\xi(W_{k}, X, y)\\]
    \\[v_k = \\beta_2 v_{k-1} + (1-\\beta_2)(\\nabla\\xi(W_{k}, X, y))^2,\\]
    and then the weights \\(W_{k}\\) are updated following the formulas:
    \\[\hat{m_k} = \\frac{m_k}{1-\\beta_1^k}\\]
    \\[\hat{v_k} = \\frac{v_k}{1-\\beta_2^k}\\]
    \\[W_{k+1} = W_k - \\frac{\\alpha}{\\sqrt{\\hat{v_k}}+\\epsilon}\\hat{m_k},\\]
    where \\(\\alpha > 0\\) is the learning rate and \\(\\beta_1, \\beta_2 \\in [0,1)\\) are decaying factors.
    The \\(\\epsilon>0\\) term ensures numerical stability and should not be too big. 

    Parameters
    ----------
    ----------
    learning_rate : float, default=0.01
        The learning rate \\(\\alpha\\) -- a positive constant (usually not greater than 1.0) that controls the magnitude of steps taken in each iteration,
        and effectively the learning speed. Note that too high learning rate may lead to overshooting.

    beta1 : float, default=0.9
        The decaying factor \\(\\beta_1\\) for the first-order momentum.

    beta2 : float, default=0.999
        The decaying factor \\(\\beta_2\\) for the second-order momentum.

    epsilon : float, default=1e-6
        A smoothing term that avoids division by zero.

    Attributes
    ----------
    ----------
    learning_rate : float
        The learning rate.

    beta1 : float
        The decaying factor.

    beta2 : float
        The decaying factor.

    epsilon : float
        A smoothing term.

    References
    ----------
    ----------
    Sebastian Ruder
        "An overview of gradient descent optimization algorithms", CoRR (2016)
        <http://arxiv.org/abs/1609.04747>

    See Also
    --------
    light_labyrinth.hyperparams.optimization.RMSprop : RMSprop optimization algorithm.
    light_labyrinth.hyperparams.optimization.Nadam : Nadam optimization algorithm.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.optimization import Adam
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             optimizer=Adam(0.001))
    """

    def __init__(self, learning_rate=0.01, beta1=0.9, beta2=0.999, epsilon=1e-6):
        super().__init__("Adam", [learning_rate, beta1, beta2, epsilon])
        self._learning_rate = learning_rate
        self._beta1 = beta1
        self._beta2 = beta2
        self._epsilon = epsilon

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def beta1(self):
        return self._beta1

    @property
    def beta2(self):
        return self._beta2

    @property
    def epsilon(self):
        return self._epsilon


class Nadam(_OptimizerBase):
    """
    Nadam (Nesterov-accelerated Adaptive Moment Estimation) optimizer class for learning Light Labyrinth models.

    A modified version of the Adam optimizer. At each iteration \\(k\\) model's weights \\(W_k\\) are updated following the formula:
    \\[W_{k+1} = W_k - \\frac{\\alpha}{\\sqrt{\\hat{v_k}}+\\epsilon}\\Big(\\beta_1\\hat{m_k} + \\frac{1-\\beta_1}{1-\\beta_1^k}\\nabla\\xi(W_{k}, X, y)\\Big)\\]
    For further details see `light_labyrinth.hyperparams.optimization.Adam` optimizer.

    Parameters
    ----------
    ----------
    learning_rate : float, default=0.01
        The learning rate \\(\\alpha\\) -- a positive constant (usually not greater than 1.0) that controls the magnitude of steps taken in each iteration,
        and effectively the learning speed. Note that too high learning rate may lead to overshooting.

    beta1 : float, default=0.9
        The decaying factor \\(\\beta_1\\) for the first-order momentum.

    beta2 : float, default=0.999
        The decaying factor \\(\\beta_2\\) for the second-order momentum.

    epsilon : float, default=1e-6
        A smoothing term that avoids division by zero.

    Attributes
    ----------
    ----------
    learning_rate : float
        The learning rate.

    beta1 : float
        The decaying factor.

    beta2 : float
        The decaying factor.

    epsilon : float
        A smoothing term.

    References
    ----------
    ----------
    Sebastian Ruder
        "An overview of gradient descent optimization algorithms", CoRR (2016)
        <http://arxiv.org/abs/1609.04747>

    See Also
    --------
    light_labyrinth.hyperparams.optimization.Adam : Adam optimization algorithm.
    light_labyrinth.hyperparams.optimization.RMSprop : RMSprop optimization algorithm.

    Examples
    --------
    >>> from light_labyrinth.hyperparams.optimization import Nadam
    >>> from light_labyrinth.dim2 import LightLabyrinthClassifier
    >>> model = LightLabyrinthClassifier(3, 3,
    ...                             optimizer=Nadam(0.001))
    """

    def __init__(self, learning_rate=0.01, beta1=0.9, beta2=0.999, epsilon=1e-6):
        super().__init__("Nadam", [learning_rate, beta1, beta2, epsilon])
        self._learning_rate = learning_rate
        self._beta1 = beta1
        self._beta2 = beta2
        self._epsilon = epsilon

    @property
    def learning_rate(self):
        return self._learning_rate

    @property
    def beta1(self):
        return self._beta1

    @property
    def beta2(self):
        return self._beta2

    @property
    def epsilon(self):
        return self._epsilon
