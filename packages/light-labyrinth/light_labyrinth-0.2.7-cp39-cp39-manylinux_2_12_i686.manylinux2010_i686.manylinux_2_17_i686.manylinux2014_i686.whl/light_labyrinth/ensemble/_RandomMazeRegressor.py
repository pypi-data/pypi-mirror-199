from sklearn.ensemble import BaggingRegressor

from ..dim2 import LightLabyrinthRandomRegressor
from ..hyperparams.activation import *
from ..hyperparams.error_function import *
from ..hyperparams.optimization import *
from ..hyperparams.regularization import *
from ..hyperparams.weights_init import LightLabyrinthWeightsInit
from ..sklearn_wrappers import SklearnRegressorWrapperModel
from ..utils import LightLabyrinthVerbosityLevel


class RandomMazeRegressor:
    """A Random Maze Regressor is an ensemble model made of several
        random 2-dimensional Light Labyrinth models. Each base regressor
        is trained on a separate bootstrap sample drawn from the training data.
        The randomness of individual base regressors lowers the variance
        of an ensemble model which in effect may yield better results than a
        standard Light Labyrinth regressor.

        ```
            +--------------------------------------------+
            | X             X              X             |
            | !__.__,       |__,__.        !__,__        |
            | |__|__!__ y0  |__|__|__ y1   |__!__|__ y2  |
            | |__|__*       |__|__*        |__!__*       |
            |                                            |
            | X             X              X             |
            | !__.__,       |__,__.        !__,__        |
            | !__|__!__ y3  |__!__|__ y4   |__!__|__ y5  |==> y
            | |__|__*       !__!__*        |__!__*       |
            |                                            |
            | X             X              X             |
            | !__,__        |__ __.        !__,__.       |
            | |__!__|__ y6  |__|__|__ y7   |__|__!__ y8  |
            | !__|__*       |__|__*        |__!__*       |
            +--------------------------------------------+
        ```

        An example of an ensemble made of `n_estimators = 9`
        random Light Labyrinths of shape `height = 3` by `width = 3`.

        Parameters
        ----------
        ----------
        height : int 
            Height of the Light Labyrinth. Note that `height > 1`.

        width : int
            Width of the Light Labyrinth. Note that `width > 1`.

        features : int or float
            Portion/number of features to be used in each node.
            If float is given it should be within range (0.0, 1.0].
            If int is given it should not be greater than n_features.

        bias : bool, default=True
            Whether to use bias in each node.

        indices : ndarray, optional, default=None
            An array of shape (height, width, n_indices + bias) including indices
            to be used at each node. If `None`, indices will be selected randomly.
            Note that passing this parameter makes all the estimators identical which
            is not recommended.

        activation : `light_labyrinth.hyperparams.activation.ReflectiveIndexCalculatorRandom`, default=`light_labyrinth.hyperparams.activation.ReflectiveIndexCalculatorRandom.random_sigmoid_dot_product`
            Activation function applied to each node's output.

            -`random_sigmoid_dot_product` - logistic function over dot product of weights and input light for a given node.

        error : `light_labyrinth.hyperparams.error_function.ErrorCalculator`, default=`light_labyrinth.hyperparams.error_function.ErrorCalculator.mean_squared_error`
            Error function optimized during training.

            -`mean_squared_error` - Mean Squared Error can be used for any classification or regression task.

            -`cross_entropy` - Cross Entropy Loss is meant primarily for classification task but it can be used for regression as well.

            -`scaled_mean_squared_error` - Adaptation of MSE meant primarily for multi-label classification.
            \tOutput values of consecutive pairs of output nodes are scaled to add up to \\(\\frac{1}{k}\\), before applying MSE.

        optimizer : object, default=`light_labyrinth.hyperparams.optimization.GradientDescent(0.01)`
            Optimization algorithm. 

            -`light_labyrinth.hyperparams.optimization.GradientDescent` - Standard Gradient Descent with constant learning rate, default: learning_rate=0.01

            -`light_labyrinth.hyperparams.optimization.RMSprop` - RMSprop optimization algorithm, default: learning_rate=0.01, rho=0.9, momentum=0.0, epsilon=1e-6

            -`light_labyrinth.hyperparams.optimization.Adam` - Adam optimization algorithm, default: learning_rate=0.01, beta1=0.9, beta2=0.999, epsilon=1e-6

            -`light_labyrinth.hyperparams.optimization.Nadam` - Adam with Nesterov momentum, default: learning_rate=0.01, beta1=0.9, beta2=0.999, epsilon=1e-6


        regularization : object, default=`light_labyrinth.hyperparams.regularization.RegularizationL1(0.01)`
            Regularization technique - either L1, L2, or None.

            `light_labyrinth.hyperparams.regularization.RegularizationNone` - No regularization.

            `light_labyrinth.hyperparams.regularization.RegularizationL1` - L1 regularization: \\(\\lambda\\sum|W|\\), default: lambda_factor=0.01

            `light_labyrinth.hyperparams.regularization.RegularizationL2` - L2 regularization: \\(\\frac{\\lambda}{2}\\sum||W||\\), default: lambda_factor=0.01

        weights: ndarray, optional, default=None
            Initial weights. If `None`, weights are set according to weights_init parameter.

        weights_init: `light_labyrinth.hyperparams.weights_init.LightLabyrinthWeightsInit`, default=`light_labyrinth.hyperparams.weights_init.LightLabyrinthWeightsInit.Default`
            Method for weights initialization.

            -`light_labyrinth.hyperparams.weights_init.LightLabyrinthWeightsInit.Default` - default initialization.

            -`light_labyrinth.hyperparams.weights_init.LightLabyrinthWeightsInit.Random` - weights are initialized randomly.

            -`light_labyrinth.hyperparams.weights_init.LightLabyrinthWeightsInit.Zeros` - weights are initialized with zeros.

        n_estimators : int, default=50
            The number of base estimators in the ensemble.

        max_samples : int or float, default=1.0
            The number of samples to draw from X to train each base estimator (with
            replacement by default, see `bootstrap` for more details).

            - If int, then draw `max_samples` samples.
            - If float, then draw `max_samples * X.shape[0]` samples.

        max_features : int or float, default=1.0
            The number of features to draw from X to train each base estimator (
            without replacement by default, see `bootstrap_features` for more
            details).

            - If int, then draw `max_features` features.
            - If float, then draw `max_features * X.shape[1]` features.

        bootstrap : bool, default=True
            Whether samples are drawn with replacement. If False, sampling
            without replacement is performed.

        bootstrap_features : bool, default=False
            Whether features are drawn with replacement.

        oob_score : bool, default=False
            Whether to use out-of-bag samples to estimate
            the generalization error. Only available if bootstrap=True.

        warm_start : bool, default=False
            When set to True, reuse the solution of the previous call to fit
            and add more estimators to the ensemble, otherwise, just fit
            a whole new ensemble.

        n_jobs : int, default=None
            The number of jobs to run in parallel for both `light_labyrinth.ensemble.RandomMazeRegressor.fit` and
            `light_labyrinth.ensemble.RandomMazeRegressor.predict`. ``None`` means 1 unless in a
            `joblib.parallel_backend` context. ``-1`` means using all
            processors.

        random_state : int, RandomState instance or None, default=None
            Controls the random resampling of the original dataset
            (sample wise and feature wise).
            If the base estimator accepts a `random_state` attribute, a different
            seed is generated for each instance in the ensemble.
            Pass an int for reproducible output across multiple function calls.

        verbose : int, default=0
            Controls the verbosity of the underlying `sklearn.ensemble.BaggingRegressor`
            when fitting and predicting.

        random_state: int, optional, default=0
            Initial random state. If 0, initial random state will be set randomly.

        Attributes
        ----------
        ----------
        #TODO

        random_state : int
            Random state passed during initialization.

        Notes
        -----
        -----
        RandomMazeRegressor uses `light_labyrinth.dim2.LightLabyrinthRandomRegressor`,
        `light_labyrinth.sklearn_wrappers.SklearnRegressorWrapperModel` from the `light_labyrinth`
        library and `BaggingRegressor` from the scikit-learn library. For further
        details see the corresponding documentation pages.

        See Also
        --------
        light_labyrinth.ensemble.RandomMaze3DClassifier : Random Maze classifier with 3-dimensional Light Labyrinths as base estimators.
        light_labyrinth.ensemble.RandomMaze2DClassifier : Random Maze classifier with 2-dimensional Light Labyrinths as base estimators.
        light_labyrinth.sklearn_wrappers.SklearnRegressorWrapperModel : A wrapper for the Light Labyrinth regressors that
            can be used as a scikit-learn model.

        Examples
        --------
        >>> from light_labyrinth.ensemble import RandomMazeRegressor
        >>> from light_labyrinth.hyperparams.weights_init import LightLabyrinthWeightsInit
        >>> from light_labyrinth.hyperparams.regularization import RegularizationL1
        >>> from light_labyrinth.hyperparams.optimization import Adam
        >>> from sklearn.datasets import fetch_openml
        >>> from sklearn.model_selection import train_test_split
        >>> from sklearn.metrics import r2_score
        >>> X, y = fetch_openml("pol", return_X_y=True)
        >>> X = X.to_numpy()
        >>> y = y.to_numpy().reshape(-1,1)
        >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        >>> ens = RandomMazeRegressor(3, 3, features=0.7, bias=True,
        ...                                optimizer=Adam(0.005),
        ...                                regularization=RegularizationL1(0.01)
        ...                                weights_init=LightLabyrinthWeightsInit.Zeros,
        ...                                n_estimators=50)
        >>> ens.fit(X_train, y_train, epochs=10, batch_size=10)
        >>> y_pred = ens.predict(X_test)
        >>> r2_score(y_test, y_pred)
        0.89
        """

    def __init__(self, height, width, features, bias=True, indices=None,
                 activation=ReflectiveIndexCalculatorRandom.random_sigmoid_dot_product,
                 error=ErrorCalculator.mean_squared_error,
                 optimizer=GradientDescent(0.01),
                 regularization=RegularizationL1(0.01),
                 weights=None,
                 weights_init=LightLabyrinthWeightsInit.Default,
                 random_state=0,
                 n_estimators=50,
                 *,
                 max_samples=1.0,
                 max_features=1.0,
                 bootstrap=True,
                 bootstrap_features=False,
                 oob_score=False,
                 warm_start=False,
                 n_jobs=None,
                 verbose=0):
        self._base_estimator = LightLabyrinthRandomRegressor(height, width, features, bias, indices,
                                                             activation,
                                                             error,
                                                             optimizer,
                                                             regularization,
                                                             weights,
                                                             weights_init,
                                                             random_state)
        self._n_estimators = n_estimators
        self._max_samples = max_samples
        self._max_features = max_features
        self._bootstrap = bootstrap
        self._bootstrap_features = bootstrap_features
        self._oob_score = oob_score
        self._warm_start = warm_start
        self._n_jobs = n_jobs
        self._random_state = random_state
        self._verbose = verbose
        self._is_fit = False

    def fit(self, X, y, epochs, batch_size=1.0, stop_change=1e-4, n_iter_check=0, epoch_check=1, X_val=None, y_val=None, verbosity=LightLabyrinthVerbosityLevel.Nothing):
        """Fit the model to data matrix X and target(s) y.

        Parameters
        ----------
        ----------
        X : ndarray of shape (n_samples, n_features)
            The input data.

        y : ndarray of shape (n_samples,) or (n_samples, n_outputs)
            The target values (class labels in classification, real numbers in
            regression).

        epochs : int
            Number of iterations to be performed. The solver iterates until convergence
            (determined by `stop_change`, `n_iter_check`) or this number of iterations.

        batch_size : int or float, default=1.0
            Size of mini-batches for stochastic optimizers given either as portion of 
            samples (float) or the exact number (int).
            When type is float, `batch_size = max(1, int(batch_size * n_samples))`.

        stop_change : float, default=1e-4
            Tolerance for the optimization. When the loss or score is not improving
            by at least ``stop_change`` for ``n_iter_check`` consecutive iterations,
            convergence is considered to be reached and training stops.

        n_iter_check : int, default=0
            Maximum number of epochs to not meet ``stop_change`` improvement.
            When set to 0, exactly ``epochs`` iterations will be performed.

        epoch_check : int, default=1
            Determines how often the condition for convergence is checked.
            `epoch_check = i` means that the condition will be checked every i-th iteration.
            When set to 0 the condition will not be checked at all and the learning history will be empty.

        X_val : ndarray of shape (n_val_samples, n_features), default=None
            The validation data. 
            If `X_val` is given, `y_val` must be given as well.

        y_val : ndarray of shape (n_val_samples,) or (n_val_samples, n_outputs), default=None
            Target values of the validation set. 
            If `y_val` is given, `X_val` must be given as well.

        verbosity: `light_labyrinth.utils.LightLabyrinthVerbosityLevel`, default=`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Nothing`
            Verbosity level.

            -`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Nothing` - No output is printed.

            -`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Basic` - Display logs about important events during the learning process. 

            -`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Full` - Detailed output from the learning process is displayed.

        Returns
        -------
        -------
        self : object
            Estimator instance. 
        """
        if self._is_fit:
            raise Exception("Model is already fit")
        self._wrapper = SklearnRegressorWrapperModel(
            self._base_estimator, epochs, batch_size, stop_change, n_iter_check, epoch_check, X_val, y_val, verbosity)
        self._clf = BaggingRegressor(base_estimator=self._wrapper,
                                     n_estimators=self._n_estimators,
                                     max_samples=self._max_samples,
                                     max_features=self._max_features,
                                     bootstrap=self._bootstrap,
                                     bootstrap_features=self._bootstrap_features,
                                     oob_score=self._oob_score,
                                     warm_start=self._warm_start,
                                     n_jobs=self._n_jobs,
                                     random_state=self._random_state,
                                     verbose=self._verbose)

        self._clf.fit(X, y)
        self._is_fit = True
        return self

    def predict(self, X):
        """Predict using the Random Maze regressor.

        Parameters
        ----------
        ----------
        X : ndarray of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        -------
        y : ndarray of shape (n_samples, 1)
            The predicted values.
        """
        if not self._is_fit:
            raise Exception("Model is not fit")
        y_pred = self._clf.predict(X)
        return y_pred
