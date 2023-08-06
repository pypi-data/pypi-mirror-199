from sklearn.base import BaseEstimator, RegressorMixin

from ..hyperparams import *
from ..utils import LightLabyrinthVerbosityLevel


class SklearnRegressorWrapperModel(RegressorMixin, BaseEstimator):
    """A wrapper class for Light Labyrinth regressors.

        `light_labyrinth.sklearn_wrappers.SklearnRegressorWrapperModel` allows to
        use Light Labyrinth models as if they were models from the Scikit-learn
        library. 

        Parameters
        ----------
        ----------
        model : object 
            Base regressor.

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

        y_val : ndarray of shape (n_val_samples, n_labels), default=None
            Target labels of the validation set. 
            If `y_val` is given, `X_val` must be given as well.

        verbosity: `light_labyrinth.utils.LightLabyrinthVerbosityLevel`, default=`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Nothing`
            Verbosity level.

            -`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Nothing` - No output is printed.

            -`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Basic` - Display logs about important events during the learning process. 

            -`light_labyrinth.utils.LightLabyrinthVerbosityLevel.Full` - Detailed output from the learning process is displayed.

        random_state : int
            Random state passed during initialization.

        Notes
        -----
        -----
        This implementation may not work with some meta-algorithms in the Scikit-learn library
        due to their specific nature. 

        See Also
        --------
        light_labyrinth.sklearn_wrappers.SklearnClassifierWrapperModel : wrapper for Light Labyrinth classifiers.

        Examples
        --------
        **Basic usage**
        >>> from light_labyrinth.sklearn_wrappers import SklearnRegressorWrapperModel
        >>> from light_labyrinth.dim2 import LightLabyrinthRegressor
        >>> from light_labyrinth.hyperparams.activation import *
        >>> from light_labyrinth.hyperparams.error_function import *
        >>> from light_labyrinth.hyperparams.regularization import *
        >>> from light_labyrinth.hyperparams.optimization import *
        >>> from sklearn.datasets import make_regression
        >>> from sklearn.model_selection import train_test_split
        >>> 
        >>> X, y = make_regression(n_samples=1000)
        >>> y = y.reshape(-1,1)
        >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        >>> 
        >>> model = LightLabyrinthRegressor(4, 4,
        ...                                 error=ErrorCalculator.mean_squared_error,
        ...                                 activation=ReflectiveIndexCalculator.sigmoid_dot_product,
        ...                                 optimizer=RMSprop(0.01),
        ...                                 regularization=RegularizationL1(0.05))
        >>> wrapped = SklearnRegressorWrapperModel(model, epochs=10, batch_size=40, X_val=X_test, y_val=y_test)
        >>> wrapped.fit(X_train, y_train)
        >>> y_pred = wrapped.predict(X_test)
        >>> print(r2_score(y_true=y_test, y_pred=y_pred))
        0.91

        **Cross validation**
        >>> from sklearn.model_selection import cross_validate
        >>> 
        >>> cv_results = cross_validate(wrapped, X_test, y_test, cv=5)
        >>> print(cv_results['test_score'])
        [0.76843525 0.89634702 0.84553729 0.85088513 0.84079953]

        **Grid Search**
        >>> from sklearn.datasets import make_regression
        >>> from sklearn.model_selection import GridSearchCV
        >>> from sklearn.pipeline import Pipeline
        >>> from sklearn.preprocessing import MinMaxScaler
        >>> from sklearn.model_selection import train_test_split
        >>> from light_labyrinth.sklearn_wrappers import SklearnRegressorWrapperModel
        >>> from light_labyrinth.hyperparams.error_function import *
        >>> from light_labyrinth.dim2 import LightLabyrinthRegressor
        >>>
        >>> X, y = make_regression(n_samples=1000)
        >>> y = y.reshape(-1,1)
        >>> X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=0)
        >>> 
        >>> model = LightLabyrinthRegressor(3, 3)
        >>>
        >>> wrapped = SklearnRegressorWrapperModel(model, epochs=10, batch_size=10)
        >>> llr_pipe = Pipeline([('mms', MinMaxScaler()),
        ...                    ('llr', wrapped)])
        >>>                    
        >>> parameters = { 'llr__width': [2, 3, 4], 'llr__height': [3, 4, 5], 'llr__error': 
        ...                [ErrorCalculator.mean_squared_error,
        ...                 ErrorCalculator.cross_entropy,
        ...                 ErrorCalculator.scaled_mean_squared_error]}
        >>>
        >>> gs = GridSearchCV(llr_pipe, parameters)
        >>> gs.fit(X_train, y_train)
        >>>
        >>> best = gs.best_estimator_
        >>> gs.cv_results_
    """

    def __init__(self, model, epochs, batch_size=1.0, stop_change=1e-4, n_iter_check=0, epoch_check=1, X_val=None, y_val=None, verbosity=LightLabyrinthVerbosityLevel.Nothing, **base_estimator_args):
        self._model = model
        self._epochs = epochs
        self._fit_params = {
            "batch_size": batch_size,
            "stop_change": stop_change,
            "n_iter_check": n_iter_check,
            "epoch_check": epoch_check,
            "X_val": X_val,
            "y_val": y_val,
            "verbosity": verbosity
        }
        self._base_estimator_params = base_estimator_args

    @property
    def model(self):
        """Base estimator.

        Returns
        -------
        model : object
            Base regressor object.
        """
        return self._model

    def get_params(self, deep=True):
        """Get parameters for this estimator.

        Parameters
        ----------
        ----------
        deep : bool, default=True
            If True, will return the parameters for this estimator and
            contained sub-objects that are estimators.

        Returns
        -------
        params : dict
            Parameter names mapped to their values.
        """
        params = {
            "model": self._model,
            "epochs": self._epochs,
            **self._fit_params,
        }
        if deep:
            return {**params, **self._base_estimator_params}
        else:
            return params

    def set_params(self, **kwargs):
        """
        Set the parameters of this estimator.

        Parameters
        ----------
        **kwargs : dict
            Estimator parameters.

        Returns
        -------
        self : estimator instance
            Estimator instance.
        """
        if model := kwargs.pop("model", None):
            self._model = model
        if epochs := kwargs.pop("epochs", None):
            self._epochs = epochs
        for param in self._fit_params.keys():
            if p := kwargs.pop(param, None):
                self._fit_params[param] = p
        self._base_estimator_params.update(kwargs)
        return self

    def fit(self, X, y):
        """Fit the model to data matrix X and targets y.

        Parameters
        ----------
        ----------
        X : ndarray of shape (n_samples, n_features)
            The input data.

        y : ndarray of shape (n_samples, 1)
            The target class labels.

        Returns
        -------
        -------
        estimator instance
            Estimator instance.
        """
        if len(y.shape) == 1:
            y = y.reshape(-1, 1)
        _ = self._model.fit(X, y, self._epochs, **self._fit_params)
        return self

    def predict(self, X):
        """Predict using the underlying Light Labyrinth regressor.

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
        return self._model.predict(X)
