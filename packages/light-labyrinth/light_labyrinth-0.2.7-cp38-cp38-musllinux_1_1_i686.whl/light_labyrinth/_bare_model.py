from ctypes import *
from ctypes import cast as ccast

import numpy as np

from ._light_labyrinth_c._light_labyrinth_c import (LightLabyrinthError,
                                                    LightLabyrinthException,
                                                    _c_Hyperparams,
                                                    _c_Hyperparams_3d,
                                                    _c_LearningProcess,
                                                    _c_LearningProcess_3d,
                                                    _c_LearningProcess_dynamic,
                                                    _c_LightLabyrinth,
                                                    _c_LightLabyrinth_3d,
                                                    _c_Matrix2d_float,
                                                    _c_Matrix3d_float,
                                                    _c_Matrix4d_float,
                                                    _c_ReflectiveDict,
                                                    _c_ReflectiveDict_3d,
                                                    _libwrapper,
                                                    _LightLabyrinthDataset)
from .hyperparams.activation import *
from .hyperparams.error_function import *
from .hyperparams.optimization import *
from .hyperparams.regularization import *
from .hyperparams.weights_init import LightLabyrinthWeightsInit
from .utils import *


class _LightLabyrinthModel:

    _DefaultWeightsInit = LightLabyrinthWeightsInit.Random

    _model_class_type_dict = {
        "_c_LightLabyrinth": _c_LightLabyrinth,
        "_c_LightLabyrinth_3d": _c_LightLabyrinth_3d
    }

    _process_class_type_dict = {
        "_c_LearningProcess": _c_LearningProcess,
        "_c_LearningProcess_3d": _c_LearningProcess_3d,
        "_c_LearningProcess_dynamic": _c_LearningProcess_dynamic
    }

    _c_fields = [
        "_model", "_process_c", "_fit_func", "_destroy_func", "_predict_func", "_destroy_process_func"
    ]

    def __init__(self, model_name, model_type, model_class_type, process, height, width, depth, bias, activation, error, optimizer, regularization, weights, weights_init, random_state):
        self._model_name = model_name
        self._model_type = model_type
        self._model_class_type = model_class_type
        self._process = process
        self._height = height
        self._width = width
        self._depth = depth
        self._bias = bias
        self._activation = activation
        self._error = error
        self._optimizer = optimizer
        self._regularization = regularization
        self._fit_func_name = f"{self._model_name}_{self._process.name}_{self._optimizer.name}_{self._regularization.name}_{self._activation.name}_{self._error.name}_fit"
        self._destroy_func_name = f"{self._model_type}_destroy"
        self._predict_func_name = f"{self._model_type}_predict"
        if weights_init is None:
            weights_init = LightLabyrinthWeightsInit.Default
        if weights is not None and weights_init != LightLabyrinthWeightsInit.Default:
            raise LightLabyrinthException(
                "Both weights and weights_init provided")
        if weights is None and weights_init == LightLabyrinthWeightsInit.Default:
            weights_init = self._DefaultWeightsInit
        self._weights = weights
        self._weights_init = weights_init
        self._random_state = random_state
        self._fitted = False
        self._set_c_fields()

    def _set_c_fields(self):
        self._model = POINTER(
            _LightLabyrinthModel._model_class_type_dict[self._model_class_type])()
        self._process_c = _LightLabyrinthModel._process_class_type_dict[self._process.class_type](
        )
        self._fit_func = _libwrapper.__getattribute__(self._fit_func_name)
        self._destroy_func = _libwrapper.__getattribute__(
            self._destroy_func_name)
        self._predict_func = _libwrapper.__getattribute__(
            self._predict_func_name)
        self._destroy_process_func = _libwrapper.__getattribute__(
            self._process.destroy_func_name)

    def fit(self, X, y, epochs, batch_size=1.0, stop_change=1e-4, n_iter_check=0, epoch_check=1,
            X_val=None, y_val=None, verbosity=LightLabyrinthVerbosityLevel.Nothing):
        if self._fitted:
            raise LightLabyrinthException(
                "Model already fitted", LightLabyrinthError.INVALID_ARGUMENT)
        if isinstance(batch_size, float):
            batch_size = max(1, int(batch_size * X.shape[0]))
        cX = _LightLabyrinthDataset(X, self.bias)
        cy = _LightLabyrinthDataset(y)
        cX_val = _LightLabyrinthDataset(
            X_val, self.bias) if X_val is not None else None
        cy_val = _LightLabyrinthDataset(
            y_val) if y_val is not None else None
        self._X = X
        self._y = y
        if self._weights is not None:
            cweights = _libwrapper._cast_to_c(self._weights)
        elif self._weights_init is LightLabyrinthWeightsInit.Zeros:
            self._weights = np.zeros(self._get_shape(X, y), dtype=np.float32)
            cweights = _libwrapper._cast_to_c(self._weights)
        else:
            cweights = None

        if verbosity == LightLabyrinthVerbosityLevel.Full:
            informative_fit_func_args = [
                f"{self._model_name=} {self._model_type=} {self._model_class_type=}",
                self._weights,
                *self._get_model_options().values(),
                self._process.name,
                *self._optimizer.options,
                *self._regularization.options,
                X, y,
                X_val, y_val,
                epochs, batch_size, stop_change, n_iter_check, epoch_check, verbosity.value, self._random_state
            ]
            print(f"Calling {self._fit_func_name} with args:\n", *(str(x) for x in informative_fit_func_args), sep="\n")

        err = self._fit_func(
            byref(self._model),
            cweights,
            *self._get_model_options().values(),
            byref(self._process_c),
            *self._optimizer.options,
            *self._regularization.options,
            cX._c_dataset, cy._c_dataset,
            cX_val._c_dataset if cX_val else None, cy_val._c_dataset if cy_val else None,
            epochs, batch_size, stop_change, n_iter_check, epoch_check, verbosity.value, self._random_state
        )
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to fit {self._model_name}", err)
        self._fitted = True
        self._weights = self._get_weights()
        if epochs != 0:
            self._history = self.get_history(self._process_c)
            self._destroy_process_func(self._process_c)
            return self._history

    def _false_fit(self):
        cX = _LightLabyrinthDataset(self._X, self.bias)
        cy = _LightLabyrinthDataset(self._y)
        cweights = _libwrapper._cast_to_c(
            self._weights) if self._weights is not None else None
        err = self._fit_func(
            byref(self._model),
            cweights,
            *self._get_model_options().values(),
            byref(self._process_c),
            *self._optimizer.options,
            *self._regularization.options,
            cX._c_dataset, cy._c_dataset,
            None, None,
            0, 0, 0.0, 0, 0, LightLabyrinthVerbosityLevel.Nothing.value, 0
        )
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to false fit {self._model_name}", err)

    def predict(self, X):
        if not self._fitted:
            raise LightLabyrinthException(
                "Model not fitted yet", LightLabyrinthError.INVALID_ARGUMENT)
        cX = _LightLabyrinthDataset(X, self.bias)
        cy = _LightLabyrinthDataset(np.zeros((X.shape[0], self._y.shape[1])))
        err = self._predict_func(self._model, cX._c_dataset, cy._c_dataset)
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to fit {self.model_name}", err)
        numpy_res = cy.as_numpy()
        return numpy_res

    @property
    def weights(self):
        return self._weights

    @property
    def history(self):
        return self._history

    @property
    def trainable_params(self):
        raise NotImplementedError("trainable_params not implemented")

    def _get_weights(self):
        if not self._fitted and self._weights is not None:
            return self._weights
        if not self._fitted:
            raise LightLabyrinthException(
                "Model not fitted yet", LightLabyrinthError.INVALID_ARGUMENT)
        if self._model_type == "light_labyrinth":
            weights = POINTER(_c_Matrix3d_float)()
            err = _libwrapper.light_labyrinth_get_weights(
                self._model, byref(weights))
            err = LightLabyrinthError(err)
            if err != LightLabyrinthError.NONE:
                raise LightLabyrinthException(
                    f"Failed to get weights of {self._model_name}", err)
        elif self._model_type == "light_labyrinth_3d":
            weights = POINTER(_c_Matrix4d_float)()
            err = _libwrapper.light_labyrinth_3d_get_weights(
                self._model, byref(weights))
            err = LightLabyrinthError(err)
            if err != LightLabyrinthError.NONE:
                raise LightLabyrinthException(
                    f"Failed to get weights of {self._model_name}", err)
        else:
            raise LightLabyrinthException(
                f"Unknown labyrinth type {self._model_type}")

        return _libwrapper._cast_to_numpy(weights)

    @property
    def bias(self):
        return self._bias

    @property
    def activation(self):
        return self._activation

    @property
    def error_function(self):
        return self._error

    @property
    def optimizer(self):
        return self._optimizer

    @property
    def regularization(self):
        return self._regularization

    @property
    def random_state(self):
        return self._random_state

    def get_history(self, process):
        raise NotImplementedError("get_history not implemented")

    def _get_model_options(self):
        return self.get_options()

    def get_options(self, deep=True):
        raise NotImplementedError("get_options not implemented")

    def get_params(self, deep=True):
        params = {
            "bias": self._bias,
            "activation": self._activation,
            "error": self._error,
            "optimizer": self._optimizer,
            "regularization": self._regularization,
            "weights": self._weights,
            "random_state": self._random_state
        }
        return {**self.get_options(), **params}

    def set_params(self, **kwargs):
        for k, v in kwargs.items():
            self.__setattribute__(f"_{k}", v)

    def _get_shape(self, X, y):
        if self._depth > 1:
            return (self._height, self._width, self._depth, 3*(X.shape[1] + int(self._bias)))
        elif self._depth == 0:
            return (self._height, self._width, y.shape[1], 3*(X.shape[1] + int(self._bias)))
        else:
            return (self._height-1, self._width-1, X.shape[1] + int(self._bias))

    def __del__(self):
        self._destroy_func(self._model)

    def __getstate__(self):
        state = {k: v for k, v in self.__dict__.items(
        ) if k not in _LightLabyrinthModel._c_fields}
        return state

    def __setstate__(self, d):
        self.__dict__ = d
        self._set_c_fields()
        if d["_fitted"]:
            self._false_fit()


class LightLabyrinth(_LightLabyrinthModel):
    def __init__(self, height, width, bias=True,
                 activation=ReflectiveIndexCalculator.sigmoid_dot_product,
                 error=ErrorCalculator.mean_squared_error,
                 optimizer=None,
                 regularization=None,
                 weights=None,
                 weights_init=LightLabyrinthWeightsInit.Default,
                 random_state=0,
                 process=None):
        optimizer, regularization, process = self._get_defaults(
            optimizer, regularization, process)
        super().__init__("light_labyrinth", "light_labyrinth", "_c_LightLabyrinth", process, height, width, 1,
                         bias, activation, error, optimizer, regularization, weights, weights_init, random_state)
        self._height = height
        self._width = width

    def _get_defaults(self, optimizer, regularization, process):
        if optimizer is None:
            optimizer = GradientDescent(0.01)
        if regularization is None:
            regularization = RegularizationL1(0.01)
        if process is None:
            process = LearningProcess()
        return (optimizer, regularization, process)

    def get_options(self):
        return {
            "height": self.height,
            "width": self.width
        }

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def trainable_params_(self):
        vector_len = self._X.shape[1] + (1 if self.bias else 0)
        trainable_vectors = (self.height-1)*(self.width-1) - \
            (self._y.shape[1]-2)*(self._y.shape[1]-1)/2
        return int(trainable_vectors * vector_len)

    def get_history(self, process):
        if not process.accs_train:
            return None
        accs_train = _libwrapper._cast_to_numpy(
            process.accs_train, process.calculated)
        errs_train = _libwrapper._cast_to_numpy(
            process.errs_train, process.calculated)
        if process.x_val_dataset:
            accs_val = _libwrapper._cast_to_numpy(
                process.accs_val, process.calculated)
            errs_val = _libwrapper._cast_to_numpy(
                process.errs_val, process.calculated)
        else:
            accs_val = None
            errs_val = None
        history = LightLabyrinthLearningHistory(
            accs_train, errs_train, accs_val, errs_val)
        return history

    def __del__(self):
        super().__del__()


class LightLabyrinth3D(_LightLabyrinthModel):
    def __init__(self, height, width, depth, bias=True,
                 activation=ReflectiveIndexCalculator3D.softmax_dotproduct_3d,
                 error=ErrorCalculator.mean_squared_error,
                 optimizer=None,
                 regularization=None,
                 weights=None,
                 weights_init=LightLabyrinthWeightsInit.Default,
                 random_state=0,
                 process=None):
        optimizer, regularization, process = self._get_defaults(
            optimizer, regularization, process)
        super().__init__("light_labyrinth_3d", "light_labyrinth_3d", "_c_LightLabyrinth_3d", process, height, width, depth,
                         bias, activation, error, optimizer, regularization, weights, weights_init, random_state)
        self._height = height
        self._width = width
        self._depth = depth

    def _get_defaults(self, optimizer, regularization, process):
        if optimizer is None:
            optimizer = GradientDescent(0.01)
        if regularization is None:
            regularization = RegularizationL1(0.01)
        if process is None:
            process = LearningProcess3D(LearningProcess3D.ProcessType.full)
        return (optimizer, regularization, process)

    def get_options(self):
        return {
            "height": self.height,
            "width": self.width,
            "depth": self.depth
        }

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def depth(self):
        return self._depth

    @property
    def trainable_params(self):
        vector_len = self._X.shape[1] + (1 if self.bias else 0)
        per_layers_outputs = self._y.shape[1]/self.depth
        per_layer_trainable_vectors = (self.weights.shape[0]-1)*(self.weights.shape[1]-1) - \
            (per_layers_outputs-2)*(per_layers_outputs-1)/2
        trainable_vectors = per_layer_trainable_vectors * (3*(self.depth - 1) + 2) + \
            2*(self.depth-1)*(self.width+self.height-2*per_layers_outputs)
        return int(trainable_vectors*vector_len)

    def get_history(self, process):
        if not process.accs_train:
            return None
        accs_train = _libwrapper._cast_to_numpy(
            process.accs_train, process.calculated)
        errs_train = _libwrapper._cast_to_numpy(
            process.errs_train, process.calculated)
        if process.x_val_dataset:
            accs_val = _libwrapper._cast_to_numpy(
                process.accs_val, process.calculated)
            errs_val = _libwrapper._cast_to_numpy(
                process.errs_val, process.calculated)
        else:
            accs_val = None
            errs_val = None
        history = LightLabyrinthLearningHistory(
            accs_train, errs_train, accs_val, errs_val)
        return history

    def __del__(self):
        super().__del__()


class LightLabyrinthDynamic(_LightLabyrinthModel):

    _DefaultWeightsInit = LightLabyrinthWeightsInit.Zeros

    def __init__(self, height, width, bias=True,
                 activation=ReflectiveIndexCalculator.sigmoid_dot_product,
                 error=ErrorCalculator.mean_squared_error,
                 optimizer=None,
                 regularization=None,
                 weights=None,
                 weights_init=LightLabyrinthWeightsInit.Default,
                 random_state=0,
                 process=None):
        optimizer, regularization, process = self._get_defaults(
            optimizer, regularization, process)
        super().__init__("light_labyrinth_dynamic", "light_labyrinth", "_c_LightLabyrinth", process, height, width, 1,
                         bias, activation, error, optimizer, regularization, weights, weights_init, random_state)
        self._height = height
        self._width = width

    def _get_defaults(self, optimizer, regularization, process):
        if optimizer is None:
            optimizer = GradientDescent(0.01)
        if regularization is None:
            regularization = RegularizationL1(0.01)
        if process is None:
            process = LearningProcessDynamic()
        return (optimizer, regularization, process)

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    def get_options(self):
        return {
            "height": self.height,
            "width": self.width
        }

    @property
    def trainable_params(self):
        vector_len = self._X.shape[1] + (1 if self.bias else 0)
        trainable_vectors = (self.height-1)*(self.width-1) - \
            (self._y.shape[1]-2)*(self._y.shape[1]-1)/2
        return int(trainable_vectors * vector_len)

    def get_history(self, process):
        if not process.calculated_epochs:
            return None
        sizes = _libwrapper._cast_to_numpy(
            process.calculated_epochs, self.height * self.width).reshape((self.height, self.width))
        accs_train_raw = _libwrapper._cast_to_numpy(
            process.accs_train, sizes.max())
        errs_train_raw = _libwrapper._cast_to_numpy(
            process.errs_train, sizes.max())
        accs_train = np.empty((self.height, self.width), dtype=object)
        errs_train = np.empty((self.height, self.width), dtype=object)
        for i in range(self.height):
            for j in range(self.width):
                accs_train[i, j] = accs_train_raw[i, j][:sizes[i, j]]
                errs_train[i, j] = errs_train_raw[i, j][:sizes[i, j]]

        if process.x_val_dataset:
            accs_val_raw = _libwrapper._cast_to_numpy(
                process.accs_val, sizes.max())
            errs_val_raw = _libwrapper._cast_to_numpy(
                process.errs_val, sizes.max())
            accs_val = np.empty((self.height, self.width), dtype=object)
            errs_val = np.empty((self.height, self.width), dtype=object)
            for i in range(self.height):
                for j in range(self.width):
                    accs_val[i, j] = accs_val_raw[i, j][:sizes[i, j]]
                    errs_val[i, j] = errs_val_raw[i, j][:sizes[i, j]]
        else:
            accs_val = None
            errs_val = None

        history = LightLabyrinthLearningHistory(
            accs_train, errs_train, accs_val, errs_val)
        return history

    def __del__(self):
        super().__del__()


class RandomLightLabyrinth(_LightLabyrinthModel):
    def __init__(self, height, width, features, bias=True, indices=None,
                 activation=ReflectiveIndexCalculatorRandom.random_sigmoid_dot_product,
                 error=ErrorCalculator.mean_squared_error,
                 optimizer=None,
                 regularization=None,
                 weights=None,
                 weights_init=LightLabyrinthWeightsInit.Default,
                 random_state=0,
                 process=None):
        optimizer, regularization, process = self._get_defaults(
            optimizer, regularization, process)
        super().__init__("random_light_labyrinth", "light_labyrinth", "_c_LightLabyrinth", process, height, width, 1,
                         bias, activation, error, optimizer, regularization, weights, weights_init, random_state)
        self._height = height
        self._width = width
        if isinstance(features, float):
            if features < 0 or features > 1:
                raise LightLabyrinthException(
                    "If features are float, they must be between 0 and 1")
        self._features = features
        self._indices = indices

    def _get_defaults(self, optimizer, regularization, process):
        if optimizer is None:
            optimizer = GradientDescent(0.01)
        if regularization is None:
            regularization = RegularizationL1(0.01)
        if process is None:
            process = LearningProcess()
        return (optimizer, regularization, process)

    def get_options(self):
        return {
            "height": self.height,
            "width": self.width,
            "features": self.features,
            "bias": self.bias,
            "indices": self.indices
        }

    def _get_model_options(self):
        options = self.get_options()
        if options["indices"] is not None:
            options["indices"] = _libwrapper._numpy_to_reflective_dict(
                options["indices"])
        if isinstance(options["features"], float):
            options["features"] = int(options["features"] * self._X.shape[1])
        return options

    @property
    def trainable_params(self):
        vector_len = self.features + (1 if self.bias else 0)
        trainable_vectors = (self.height-1)*(self.width-1) - \
            (self._y.shape[1]-2)*(self._y.shape[1]-1)/2
        return int(trainable_vectors * vector_len)

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def features(self):
        return self._features

    @property
    def indices(self):
        return self._indices

    def fit(self, X, y, epochs, batch_size, stop_change=1e-4, n_iter_check=0, epoch_check=1, X_val=None, y_val=None, verbosity=LightLabyrinthVerbosityLevel.Nothing):
        hist = super().fit(X, y, epochs, batch_size, stop_change,
                           n_iter_check, epoch_check, X_val, y_val, verbosity)
        rdict = self._get_reflective_dict()
        self._indices = _libwrapper._reflective_dict_to_numpy(rdict)
        return hist

    def get_history(self, process):
        if not process.accs_train:
            return None
        accs_train = _libwrapper._cast_to_numpy(
            process.accs_train, process.calculated)
        errs_train = _libwrapper._cast_to_numpy(
            process.errs_train, process.calculated)
        if process.x_val_dataset:
            accs_val = _libwrapper._cast_to_numpy(
                process.accs_val, process.calculated)
            errs_val = _libwrapper._cast_to_numpy(
                process.errs_val, process.calculated)
        else:
            accs_val = None
            errs_val = None
        history = LightLabyrinthLearningHistory(
            accs_train, errs_train, accs_val, errs_val)
        return history

    def _get_reflective_dict(self):
        hyperparams = _c_Hyperparams()
        err = _libwrapper.light_labyrinth_hyperparams_get(
            self._model, byref(hyperparams))
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                "Failed to get hyperparams of Random Light Labyrinth", err)
        rdict = ccast(hyperparams.user_data, POINTER(_c_ReflectiveDict))
        return rdict

    def _get_shape(self, X, y):
        if isinstance(self._features, float):
            features_int = int(self._features * X.shape[1])
        else:
            features_int = self._features
        return (self._height-1, self._width-1, features_int + int(self._bias))

    def __del__(self):
        if self._model:
            rdict = self._get_reflective_dict()
            _libwrapper.reflective_dict_destroy(rdict)
        super().__del__()


class RandomLightLabyrinth3D(_LightLabyrinthModel):
    def __init__(self, height, width, depth, features, bias=True, indices=None,
                 activation=ReflectiveIndexCalculator3DRandom.random_3d_softmax_dotproduct,
                 error=ErrorCalculator.mean_squared_error,
                 optimizer=None,
                 regularization=None,
                 weights=None,
                 weights_init=LightLabyrinthWeightsInit.Default,
                 random_state=0,
                 process=None):
        optimizer, regularization, process = self._get_defaults(
            optimizer, regularization, process)
        super().__init__("random_light_labyrinth_3d", "light_labyrinth_3d", "_c_LightLabyrinth_3d", process, height, width, depth,
                         bias, activation, error, optimizer, regularization, weights, weights_init, random_state)
        self._height = height
        self._width = width
        self._depth = depth
        if isinstance(features, float):
            if features < 0 or features > 1:
                raise LightLabyrinthException(
                    "If features are float, they must be between 0 and 1")
        self._features = features
        self._indices = indices

    def _get_defaults(self, optimizer, regularization, process):
        if optimizer is None:
            optimizer = GradientDescent(0.01)
        if regularization is None:
            regularization = RegularizationL1(0.01)
        if process is None:
            process = LearningProcess3D(LearningProcess3D.ProcessType.full)
        return (optimizer, regularization, process)

    def get_options(self):
        return {
            "height": self.height,
            "width": self.width,
            "depth": self.depth,
            "features": self.features,
            "bias": self.bias,
            "indices": self.indices
        }

    def _get_model_options(self):
        options = self.get_options()
        if options["indices"] is not None:
            options["indices"] = _libwrapper._numpy_to_reflective_dict_3d(
                options["indices"])
        if isinstance(options["features"], float):
            options["features"] = int(options["features"] * self._X.shape[1])
        return options

    @property
    def height(self):
        return self._height

    @property
    def width(self):
        return self._width

    @property
    def depth(self):
        return self._depth

    @property
    def features(self):
        return self._features

    @property
    def indices(self):
        return self._indices

    @property
    def trainable_params(self):
        vector_len = self.features + (1 if self.bias else 0)
        per_layers_outputs = self._y.shape[1]/self.depth
        per_layer_trainable_vectors = (self.weights.shape[0]-1)*(self.weights.shape[1]-1) - \
            (per_layers_outputs-2)*(per_layers_outputs-1)/2
        trainable_vectors = per_layer_trainable_vectors * (3*(self.depth - 1) + 2) + \
            2*(self.depth-1)*(self.width+self.height-2*per_layers_outputs)
        return int(trainable_vectors*vector_len)

    def fit(self, X, y, epochs, batch_size, stop_change=1e-4, n_iter_check=0, epoch_check=1, X_val=None, y_val=None, verbosity=LightLabyrinthVerbosityLevel.Nothing):
        hist = super().fit(X, y, epochs, batch_size, stop_change,
                           n_iter_check, epoch_check, X_val, y_val, verbosity)
        rdict = self._get_reflective_dict()
        self._indices = _libwrapper._reflective_dict_3d_to_numpy(rdict)
        return hist

    def get_history(self, process):
        if not process.accs_train:
            return None
        accs_train = _libwrapper._cast_to_numpy(
            process.accs_train, process.calculated)
        errs_train = _libwrapper._cast_to_numpy(
            process.errs_train, process.calculated)
        if process.x_val_dataset:
            accs_val = _libwrapper._cast_to_numpy(
                process.accs_val, process.calculated)
            errs_val = _libwrapper._cast_to_numpy(
                process.errs_val, process.calculated)
        else:
            accs_val = None
            errs_val = None
        history = LightLabyrinthLearningHistory(
            accs_train, errs_train, accs_val, errs_val)
        return history

    def _get_reflective_dict(self):
        hyperparams = _c_Hyperparams_3d()
        err = _libwrapper.light_labyrinth_3d_hyperparams_get(
            self._model, byref(hyperparams))
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                "Failed to get hyperparams of Random Light Labyrinth 3D", err)
        rdict = ccast(hyperparams.user_data, POINTER(_c_ReflectiveDict_3d))
        return rdict

    def _get_shape(self, X, y):
        if isinstance(self._features, float):
            features_int = int(self._features * X.shape[1])
        else:
            features_int = self._features
        return (self._height, self._width, self._depth, 3*(features_int + int(self._bias)))

    def __del__(self):
        if self._model:
            rdict = self._get_reflective_dict()
            _libwrapper.reflective_dict_3d_destroy(rdict)
        super().__del__()
