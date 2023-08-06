import numpy as np
import pandas as pd

from .._bare_model import LightLabyrinth3D
from .._tools import _MixedOutputTransformer
from ..hyperparams.activation import *
from ..hyperparams.error_function import *
from ..hyperparams.optimization import *
from ..hyperparams.regularization import *
from ..hyperparams.weights_init import LightLabyrinthWeightsInit
from ..utils import LearningProcess3D, LightLabyrinthVerbosityLevel


class LightLabyrinth3DMixedOutputPredictor(LightLabyrinth3D):
    """A mixed output Light Labyrinth model.

        The 3-dimensional version of the Light Labyrinth model
        meant for mixed output prediction is built by stacking
        several levels of 2-dimensional models and connecting all
        non-output nodes of adjacent levels with vertical upward edges.
        Each level has exactly two outputs -- for regression (lower 
        levels) one is omitted and the other serves as the part of the 
        final `k`-dimensional output; for classification (upper levels)
        each level is responsible for a single label, and the highest
        positive to negative intensity ratio per N levels of a given
        target indicates the final classification result.
        Since all the level are connected, and not independent from
        one another, this model should be able to take advantage of
        correlations between targets.

        ```
            X                     
            |__ __ 
            |__|__|
            |__|__|__ y0
            |__|__*      __ __ 
                        |__|__|
                        |__|__|__ y1A+
                        |__|__ y1A-  __ __  
                                    |__|__|
                                    |__|__|__ y2X+
                                    |__|__ y2X-  __ __  
                                                |__|__|
                                                |__|__|__ y2Y+
                                                |__|__ y2Y-  __ __  
                                                            |__|__|
                                                            |__|__|__ y2Z+
                                                            |__|__ y2Z-
        ```

        An example of `height = 4` by `width = 3` model with `k = 3` 
        target outputs. The first output (y0) yields continuous values
        (regression), the second output (y1) yields binary labels A+/A-
        (binary classification). The third output (y2) yields either 
        one of three categories: X, Y, or Z (multi-class classification).
        Note that all non-output nodes are connected with the 
        corresponding node on the lower level. 

        Parameters
        ----------
        ----------
        height : int 
            Height of the Light Labyrinth. Note that `height > 1`.

        width : int
            Width of the Light Labyrinth. Note that `width > 1`.

        bias : bool, default=True
            Whether to use bias in each node.

        activation : `light_labyrinth.hyperparams.activation.ReflectiveIndexCalculator3D`, default=`light_labyrinth.hyperparams.activation.ReflectiveIndexCalculator3D.softmax_dotproduct_3d`
            Activation function applied to each node's output.

            -`softmax_dotproduct_3d` - softmax function over product of weights and input light, for a given node.

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

        random_state: int, optional, default=0
            Initial random state. If 0, initial random state will be set randomly.

        Attributes
        ----------
        ----------
        height : int
            Height of the LightLabyrinth.

        width : int
            Width of the LightLabyrinth.

        depth : int
            Depth of the LightLabyrinth given by the number of target values.
            Note that before fitting depth is set to 0.

        trainable_params : int
            Number of trainable parameters.

        weights : ndarray of shape (height, width, n_targets, 3*(n_features + bias))
            Array of weights optimized during training. If bias is set to False, n_features is equal to the number of features in the training set X.
            If bias is set to True, n_features is increased by 1.

        history : `light_labyrinth.utils.LightLabyrinthLearningHistory`
            Learning history including error on training and (if provided) validation sets.

        bias : bool
            Boolean value whether the model was trained with bias.

        activation : `light_labyrinth.hyperparams.activation.ReflectiveIndexCalculator3D`
            Activation function used for training.

        error_function : `light_labyrinth.hyperparams.error_function.ErrorCalculator`
            Error function used for training.

        optimizer : object
            Optimization algorithm used for training, including its parameters.

        regularization : object
            Regularization used during training, including its parameters.

        random_state : int
            Random state passed during initialization.

        Notes
        -----
        -----
        LightLabyrinth3D trains iteratively. At each time step
        the partial derivatives of the loss function with respect to the model
        parameters are computed to update the weights.

        It can also have a regularization term added to the loss function
        that shrinks model parameters to prevent overfitting.

        This implementation works with data represented as dense numpy arrays
        of floating point values as well as pandas DataFrames with numeric 
        and categorical column types.

        See Also
        --------
        light_labyrinth.multioutput.LightLabyrinth3DMultioutputRegressor : 3-dimensional Light Labyrinth multioutput regressor.
        light_labyrinth.multioutput.LightLabyrinth3DMultilabelClassifier : 3-dimensional Light Labyrinth for multilabel classification.
        light_labyrinth.multioutput.LightLabyrinth3DRandomMultioutputRegressor : random Light Labyrinth regressor for multioutput regression.

        Examples
        --------
        >>> X, y = make_classification(n_samples=1000, n_classes=4, n_informative=3, random_state=42)
        >>> y1 = pd.DataFrame([f"y1{i % 3}" for i in y])
        >>> y2 = pd.DataFrame([f"y2{i**2}" for i in y])
        >>> y3 = pd.DataFrame(y, dtype=np.float64)
        >>> y2 = y2.rename(columns={0:1})
        >>> y3 = y3.rename(columns={0:2})
        >>> y = pd.concat((y1, y2, y3), axis=1)
        >>> 
        >>> y = pd.DataFrame(y)
        >>> X = pd.DataFrame(X)
        >>> 
        >>> X_train, X_test, y_train, y_test = train_test_split(X, y, stratify=y, random_state=1)
        >>> 
        >>> model = LightLabyrinth3DMixedOutputPredictor(6, 6,
        ...                             error=ErrorCalculator.scaled_mean_squared_error,
        ...                             optimizer=RMSprop(0.001),
        ...                             regularization=RegularizationL1(0.0001),
        ...                             weights_init=LightLabyrinthWeightsInit.Zeros,
        ...                             random_state=42)
        >>> 
        >>> model.fit(X_train, y_train, epochs=20, batch_size=0.02, X_val=X_test, y_val=y_test, verbosity=LightLabyrinthVerbosityLevel.Full)
        >>> y_pred = model.predict(X_test)
        >>> 
        >>> print(accuracy_score(y_true=y_test.loc[:,0], y_pred=y_pred.loc[:,0]))
        0.808
        >>> print(accuracy_score(y_true=y_test.loc[:,1], y_pred=y_pred.loc[:,1]))
        0.812
        >>> print(r2_score(y_true=y_test.loc[:,2], y_pred=y_pred.loc[:,2]))
        0.7013188528698737
        """

    def __init__(self, height, width, bias=True,
                 activation=ReflectiveIndexCalculator3D.softmax_dotproduct_3d,
                 error=ErrorCalculator.mean_squared_error,
                 optimizer=GradientDescent(0.01),
                 regularization=RegularizationL1(0.01),
                 weights=None,
                 weights_init=LightLabyrinthWeightsInit.Default,
                 random_state=0):
        super().__init__(height, width, 0, bias,
                         activation,
                         error,
                         optimizer,
                         regularization,
                         weights,
                         weights_init,
                         random_state,
                         LearningProcess3D(LearningProcess3D.ProcessType.multilabel))

    def fit(self, X, y, epochs, batch_size=1.0, stop_change=1e-4, n_iter_check=0, epoch_check=1, X_val=None, y_val=None, verbosity=LightLabyrinthVerbosityLevel.Nothing):
        """Fit the model to data matrix X and targets y.

        Parameters
        ----------
        ----------
        X : ndarray or DataFrame of shape (n_samples, n_features)
            The input data.

        y : DataFrame of shape (n_samples, n_targets)
            The target values - any combination of floating point values 
            and discrete labels.

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

        Returns
        -------
        -------
        hist : object
            Returns a `light_labyrinth.utils.LightLabyrinthLearningHistory` object with fields: 
            accs_train, accs_val, errs_train, errs_val.
        """
        # column names of `y` DataFrame must be unique
        self._check_unique_names(y)

        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        
        # get categorical and numerical column names
        num_col_names = [i[0] for i in y.dtypes.iteritems() if np.issubdtype(i[1], np.floating)]
        cat_col_names = list(set(y.columns) - set(num_col_names))
        cat_cols = [y[i].astype("category") for i in cat_col_names]

        # calculate depth (number of levels) of the Light Labyrinth
        self._depth = len(num_col_names) + sum(len(i.cat.categories) for i in cat_cols)

        # prepare target output intensities
        self._encoder = _MixedOutputTransformer(cat_col_names, num_col_names)
        y_transformed = self._encoder.fit_transform(y)
        y_val_transformed = self._encoder.transform(y_val) if y_val is not None else None

        return super().fit(X, y_transformed, epochs, batch_size, stop_change, n_iter_check, epoch_check, X_val, y_val_transformed, verbosity)

    def predict(self, X):
        """Predict using the Light Labyrinth mixed output predictor.

        Parameters
        ----------
        ----------
        X : ndarray or DataFrame of shape (n_samples, n_features)
            The input data.

        Returns
        -------
        -------
        y : DataFrame of shape (n_samples, n_targets)
            The predicted values.
        """
        if isinstance(X, pd.DataFrame):
            X = X.to_numpy()
        y_pred = super().predict(X)
        transformed = self._encoder.inverse_transform(y_pred)
        return transformed

    def __del__(self):
        super().__del__()

    def _check_unique_names(self, y):
        if len(y.columns) != len(set(y.columns)):
            raise RuntimeError("Columns must have unique names")
