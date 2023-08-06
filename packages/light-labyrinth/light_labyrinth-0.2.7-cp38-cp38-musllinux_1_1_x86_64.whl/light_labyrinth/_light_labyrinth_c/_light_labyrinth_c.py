
_package = True
#WARNING - this code is entirely generated and changes here will be overwritten#
#DO NOT MODIFY DIRECTLY!#

from enum import Enum
from ctypes import *
import numpy as np
import math
import warnings
import os
import sys
from typing import *
import pathlib
from .py_utils import *

float_ctype = c_float
uint_ctype = c_uint32
enum_ctype = c_int
float_dtype = np.float32
uint_dtype = np.uint32


def API_FP(*arguments):
    return CFUNCTYPE(enum_ctype, *arguments)


light_labyrinth_reflective_index_calculator_ctype = \
    API_FP(POINTER(float_ctype), uint_ctype, POINTER(float_ctype),
           uint_ctype, POINTER(float_ctype), uint_ctype, uint_ctype, c_void_p)

light_labyrinth_reflective_index_calculator_derivative_ctype = \
    API_FP(POINTER(float_ctype), uint_ctype, POINTER(float_ctype),
           uint_ctype, POINTER(float_ctype), uint_ctype, uint_ctype, c_void_p)

light_labyrinth_error_calculator_ctype = \
    API_FP(POINTER(float_ctype), POINTER(float_ctype), uint_ctype,
           POINTER(float_ctype), c_void_p)

light_labyrinth_error_calculator_derivative_ctype = \
    API_FP(POINTER(float_ctype), POINTER(float_ctype), uint_ctype,
           POINTER(float_ctype), c_void_p)


class _c_Hyperparams(Structure):
    _fields_ = [
        ("height", uint_ctype),
        ("width", uint_ctype),
        ("vector_len", uint_ctype),
        ("input_len", uint_ctype),
        ("outputs", uint_ctype),
        ("random_state", c_uint32),
        ("reflective_index_calculator",
         light_labyrinth_reflective_index_calculator_ctype),
        ("reflective_index_calculator_derivative",
         light_labyrinth_reflective_index_calculator_derivative_ctype),
        ("error_calculator",
         light_labyrinth_error_calculator_ctype),
        ("error_calculator_derivative",
         light_labyrinth_error_calculator_derivative_ctype),
        ("user_data", c_void_p)
    ]


class _c_LightLabyrinth(Structure):
    pass

class _c_Dataset(c_void_p):
    pass

class _c_Lcg(c_void_p):
    pass

light_labyrinth_batch_finished_callback_ctype = \
    API_FP(POINTER(_c_LightLabyrinth), POINTER(_c_Dataset), POINTER(_c_Dataset),
           uint_ctype, uint_ctype, uint_ctype, c_void_p)


class _c_Fitparams(Structure):
    _fields_ = [
        ("epochs", uint_ctype),
        ("batch_size", uint_ctype),
        ("batch_callback", light_labyrinth_batch_finished_callback_ctype),
        ("batch_callback_data", c_void_p)
    ]


class _c_Matrix2d_float(Structure):
    _fields_ = [
        ("array", POINTER(float_ctype)),
        ("height", uint_ctype),
        ("width", uint_ctype),
        ("total_size", uint_ctype),
        ("is_view", c_bool)
    ]


class _c_Matrix3d_float(Structure):
    _fields_ = [
        ("array", POINTER(float_ctype)),
        ("height", uint_ctype),
        ("width", uint_ctype),
        ("inner_size", uint_ctype),
        ("total_size", uint_ctype),
        ("is_view", c_bool)
    ]


class _c_Matrix4d_float(Structure):
    _fields_ = [
        ("array", POINTER(float_ctype)),
        ("height", uint_ctype),
        ("width", uint_ctype),
        ("inner_height", uint_ctype),
        ("inner_width", uint_ctype),
        ("total_size", uint_ctype),
        ("is_view", c_bool)
    ]


class _c_Matrix5d_float(Structure):
    _fields_ = [
        ("array", POINTER(float_ctype)),
        ("dims", uint_ctype*5),
        ("total_size", uint_ctype),
        ("is_view", c_bool)
    ]


optimizer_function_ctype = \
    API_FP(POINTER(float_ctype), POINTER(float_ctype), POINTER(float_ctype),
           uint_ctype, uint_ctype, c_void_p)


class _c_Optimizer(Structure):
    pass


optimizer_destoryer_ctype = \
    API_FP(_c_Optimizer)

_c_Optimizer._fields_ = [
    ("optimizer_function", optimizer_function_ctype),
    ("destroyer", optimizer_destoryer_ctype),
    ("user_data", c_void_p)
]


regularization_function = \
    API_FP(POINTER(float_ctype), uint_ctype,
           POINTER(float_ctype), uint_ctype, c_void_p)

regularization_function_gradient = \
    API_FP(POINTER(float_ctype), uint_ctype,
           POINTER(float_ctype), uint_ctype, c_void_p)


class _c_Regularization(Structure):
    pass


regularizer_destoryer_ctype = \
    API_FP(_c_Regularization)

_c_Regularization._fields_ = [
    ("regularization", regularization_function),
    ("regularization_gradient", regularization_function_gradient),
    ("destroyer", regularizer_destoryer_ctype),
    ("user_data", c_void_p)
]


class _c_LightLabyrinth_3d(Structure):
    pass


light_labyrinth_3d_batch_finished_callback_ctype = \
    API_FP(POINTER(_c_LightLabyrinth_3d), POINTER(_c_Dataset), POINTER(_c_Dataset),
           uint_ctype, uint_ctype, uint_ctype, c_void_p)


class _c_Fitparams_3d(Structure):
    _fields_ = [
        ("epochs", uint_ctype),
        ("batch_size", uint_ctype),
        ("batch_callback", light_labyrinth_3d_batch_finished_callback_ctype),
        ("batch_callback_data", c_void_p)
    ]


light_labyrinth_3d_reflective_index_calculator_ctype = \
    API_FP(POINTER(float_ctype), uint_ctype, POINTER(float_ctype),
           uint_ctype, POINTER(float_ctype), uint_ctype, uint_ctype, uint_ctype, c_void_p)

light_labyrinth_3d_reflective_index_calculator_derivative_ctype = \
    API_FP(POINTER(float_ctype), uint_ctype, POINTER(float_ctype),
           uint_ctype, POINTER(_c_Matrix2d_float), uint_ctype, uint_ctype, uint_ctype, c_void_p)

light_labyrinth_3d_error_calculator_ctype = \
    API_FP(POINTER(float_ctype), POINTER(float_ctype), uint_ctype,
           POINTER(float_ctype), c_void_p)

light_labyrinth_3d_error_calculator_derivative_ctype = \
    API_FP(POINTER(float_ctype), POINTER(float_ctype), uint_ctype,
           POINTER(float_ctype), c_void_p)


class _c_Hyperparams_3d(Structure):
    _fields_ = [
        ("height", uint_ctype),
        ("width", uint_ctype),
        ("depth", uint_ctype),
        ("vector_len", uint_ctype),
        ("input_len", uint_ctype),
        ("outputs_per_level", uint_ctype),
        ("outputs_total", uint_ctype),
        ("random_state", c_uint32),
        ("reflective_index_calculator",
         light_labyrinth_reflective_index_calculator_ctype),
        ("reflective_index_calculator_derivative",
         light_labyrinth_reflective_index_calculator_derivative_ctype),
        ("error_calculator",
         light_labyrinth_3d_error_calculator_ctype),
        ("error_calculator_derivative",
         light_labyrinth_3d_error_calculator_derivative_ctype),
        ("user_data", c_void_p)
    ]


class _c_LearningProcess(Structure):
    _fields_ = [
        ("accs_train", POINTER(float_ctype)),
        ("accs_val", POINTER(float_ctype)),
        ("errs_train", POINTER(float_ctype)),
        ("errs_val", POINTER(float_ctype)),
        ("buffer", POINTER(float_ctype)),
        ("calculated", uint_ctype),
        ("epochs", uint_ctype),
        ("epoch_check", uint_ctype),
        ("res_size", uint_ctype),
        ("stop_change", float_ctype),
        ("n_iter_check", uint_ctype),
        ("min_error_index", uint_ctype),
        ("y_pred_train", POINTER(_c_Dataset)),
        ("y_pred_val", POINTER(_c_Dataset)),
        ("x_val_dataset", POINTER(_c_Dataset)),
        ("y_val_dataset", POINTER(_c_Dataset))
    ]


class _c_LearningProcess_3d(Structure):
    _fields_ = [
        ("accs_train", POINTER(float_ctype)),
        ("accs_val", POINTER(float_ctype)),
        ("errs_train", POINTER(float_ctype)),
        ("errs_val", POINTER(float_ctype)),
        ("buffer", POINTER(float_ctype)),
        ("calculated", uint_ctype),
        ("epochs", uint_ctype),
        ("epoch_check", uint_ctype),
        ("res_size", uint_ctype),
        ("stop_change", float_ctype),
        ("n_iter_check", uint_ctype),
        ("min_error_index", uint_ctype),
        ("y_pred_train", POINTER(_c_Dataset)),
        ("y_pred_val", POINTER(_c_Dataset)),
        ("x_val_dataset", POINTER(_c_Dataset)),
        ("y_val_dataset", POINTER(_c_Dataset))
    ]


class _c_LearningProcess_dynamic(Structure):
    _fields_ = [
        ("accs_train", POINTER(_c_Matrix3d_float)),
        ("accs_val", POINTER(_c_Matrix3d_float)),
        ("errs_train", POINTER(_c_Matrix3d_float)),
        ("errs_val", POINTER(_c_Matrix3d_float)),
        ("buffer", POINTER(float_ctype)),
        ("epochs", uint_ctype),
        ("epoch_check", uint_ctype),
        ("res_size", uint_ctype),
        ("stop_change", float_ctype),
        ("n_iter_check", uint_ctype),
        ("min_error_index", uint_ctype),
        ("calculated_epochs", POINTER(uint_ctype)),
        ("y_pred_train", POINTER(_c_Dataset)),
        ("y_pred_val", POINTER(_c_Dataset)),
        ("x_val_dataset", POINTER(_c_Dataset)),
        ("y_val_dataset", POINTER(_c_Dataset))
    ]


class _c_ReflectiveDict(Structure):
    _fields_ = [
        ("height", uint_ctype),
        ("width", uint_ctype),
        ("mirror_len", uint_ctype),
        ("total_size", uint_ctype),
        ("indices", POINTER(uint_ctype))
    ]

class _c_ReflectiveDict_3d(Structure):
    _fields_ = [
        ("height", uint_ctype),
        ("width", uint_ctype),
        ("depth", uint_ctype),
        ("mirror_len", uint_ctype),
        ("total_size", uint_ctype),
        ("indices", POINTER(uint_ctype))
    ]

class LightLabyrinthError(Enum):
    NONE = 0
    OUT_OF_MEMORY = 1
    DIVISION_BY_ZERO = 2
    INVALID_ARGUMENT = 3
    NOT_IMPLEMENTED = 4
    INVALID_DIMENSION = 5
    FUNCTION_NOT_SET = 6
    NO_FILE_ACCESS = 7
    INVALID_VALUE = 8
    STOP_PROCESSING = 9

class LightLabyrinthVerbosityLevel(Enum):
    Nothing = 0
    Basic = 1
    Full = 2

class LightLabyrinthException(Exception):
    def __init__(self, msg, error = None, *args, **kwargs):
        super().__init__(msg, [error, *args], **kwargs)
        self.error = error

class _LightLabyrinthLibWrapper:

    def __init__(self, path: str):
        self.dll = cdll.LoadLibrary(path)

        if getattr(self.dll, "python_module_output_set_py_print", False):
            @CFUNCTYPE(None, c_char_p)
            def _py_print(msg):
                print(msg.decode(), end="")
            self._py_print = _py_print
            self.dll.python_module_output_set_py_print(_py_print)

        # Dataset
        self._wrap_function("dataset_create",
                            [POINTER(POINTER(_c_Dataset)), uint_ctype, uint_ctype])

        self._wrap_function("dataset_create_from_1d_array",
                            [POINTER(POINTER(_c_Dataset)), POINTER(float_ctype), uint_ctype, uint_ctype])

        self._wrap_function("dataset_get_data",
                            [POINTER(_c_Dataset), POINTER(POINTER(float_ctype)), POINTER(uint_ctype)])

        self._wrap_function("dataset_destroy",
                            [POINTER(_c_Dataset)])

        # LightLabyrinth
        self._wrap_function("light_labyrinth_create",
                            [POINTER(POINTER(_c_LightLabyrinth)), POINTER(_c_Hyperparams), _c_Optimizer, _c_Regularization])

        self._wrap_function("light_labyrinth_create_set_weights",
                            [POINTER(POINTER(_c_LightLabyrinth)), POINTER(_c_Hyperparams), _c_Optimizer, _c_Regularization, POINTER(_c_Matrix3d_float)])

        self._wrap_function("light_labyrinth_get_weights",
                            [POINTER(_c_LightLabyrinth), POINTER(POINTER(_c_Matrix3d_float))])

        self._wrap_function("light_labyrinth_set_weights",
                            [POINTER(_c_LightLabyrinth), POINTER(_c_Matrix3d_float)])

        self._wrap_function("light_labyrinth_fit",
                            [POINTER(_c_LightLabyrinth), POINTER(_c_Dataset), POINTER(_c_Dataset), _c_Fitparams])

        self._wrap_function("light_labyrinth_predict",
                            [POINTER(_c_LightLabyrinth), POINTER(_c_Dataset), POINTER(_c_Dataset)])

        self._wrap_function("light_labyrinth_hyperparams_get",
                            [POINTER(_c_LightLabyrinth), POINTER(_c_Hyperparams)])

        self._wrap_function("light_labyrinth_optimizer_get",
                            [POINTER(_c_LightLabyrinth), POINTER(_c_Optimizer)])

        self._wrap_function("light_labyrinth_regularization_get",
                            [POINTER(_c_LightLabyrinth), POINTER(_c_Regularization)])

        self._wrap_function("light_labyrinth_destroy",
                            [POINTER(_c_LightLabyrinth)])

        # LightLabyrinth3D
        self._wrap_function("light_labyrinth_3d_create",
                            [POINTER(POINTER(_c_LightLabyrinth_3d)), POINTER(_c_Hyperparams), _c_Optimizer, _c_Regularization])

        self._wrap_function("light_labyrinth_3d_create_set_weights",
                            [POINTER(POINTER(_c_LightLabyrinth_3d)), POINTER(_c_Hyperparams), _c_Optimizer, _c_Regularization, POINTER(_c_Matrix4d_float)])

        self._wrap_function("light_labyrinth_3d_get_weights",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(POINTER(_c_Matrix4d_float))])

        self._wrap_function("light_labyrinth_3d_set_weights",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Matrix4d_float)])

        self._wrap_function("light_labyrinth_3d_fit",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Dataset), POINTER(_c_Dataset), _c_Fitparams_3d])

        self._wrap_function("light_labyrinth_3d_predict",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Dataset), POINTER(_c_Dataset)])

        self._wrap_function("light_labyrinth_3d_hyperparams_get",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Hyperparams_3d)])

        self._wrap_function("light_labyrinth_3d_optimizer_get",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Optimizer)])

        self._wrap_function("light_labyrinth_3d_regularization_get",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Regularization)])

        self._wrap_function("light_labyrinth_3d_destroy",
                            [POINTER(_c_LightLabyrinth_3d)])

        
        # LearningCallback
        self._wrap_function("fill_learning_process",
                            [POINTER(_c_LearningProcess), uint_ctype, uint_ctype, uint_ctype, float_ctype,
                            uint_ctype, uint_ctype,
                            POINTER(_c_Dataset), POINTER(_c_Dataset)])

        self._wrap_function("free_learning_process",
                            [POINTER(_c_LearningProcess)])

        self._wrap_function("learning_callback_full",
                            [POINTER(_c_LightLabyrinth), POINTER(_c_Dataset), POINTER(_c_Dataset), uint_ctype, uint_ctype, uint_ctype, c_void_p])

        # LearningCallback3D
        self._wrap_function("fill_learning_process_3d",
                            [POINTER(_c_LearningProcess_3d), uint_ctype, uint_ctype, uint_ctype, float_ctype,
                            uint_ctype, uint_ctype,
                            POINTER(_c_Dataset), POINTER(_c_Dataset)])

        self._wrap_function("free_learning_process_3d",
                            [POINTER(_c_LearningProcess_3d)])

        self._wrap_function("learning_callback_full_3d",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Dataset), POINTER(_c_Dataset), uint_ctype, uint_ctype, uint_ctype, c_void_p])

        self._wrap_function("learning_callback_multilabel_full_3d",
                            [POINTER(_c_LightLabyrinth_3d), POINTER(_c_Dataset), POINTER(_c_Dataset), uint_ctype, uint_ctype, uint_ctype, c_void_p])

        # LearningCallbackDynamic
        self._wrap_function("fill_learning_process_dynamic",
                            [POINTER(_c_LearningProcess_dynamic), uint_ctype, uint_ctype, uint_ctype, uint_ctype,
                            uint_ctype, float_ctype, uint_ctype, uint_ctype,
                            POINTER(_c_Dataset), POINTER(_c_Dataset)])

        self._wrap_function("free_learning_process_dynamic",
                            [POINTER(_c_LearningProcess_dynamic)])

        self._wrap_function("learning_callback_full_dynamic",
                            [POINTER(_c_LearningProcess_dynamic), POINTER(_c_Dataset), POINTER(_c_Dataset), uint_ctype, uint_ctype, uint_ctype, c_void_p])

        # Optimizer
        # gradient_descent
        self._wrap_function("optimizer_Gradient_Descent_create",
                            [POINTER(_c_Optimizer), float_ctype, float_ctype])

        # RMSprop
        self._wrap_function("optimizer_RMSprop_create",
                            [POINTER(_c_Optimizer), float_ctype, float_ctype, float_ctype, float_ctype, uint_ctype])

        # Adam
        self._wrap_function("optimizer_Adam_create",
                            [POINTER(_c_Optimizer), float_ctype, float_ctype, float_ctype, float_ctype, uint_ctype])

        # Nadam
        self._wrap_function("optimizer_Nadam_create",
                            [POINTER(_c_Optimizer), float_ctype, float_ctype, float_ctype, float_ctype, uint_ctype])

        # Regularization
        # None
        self._wrap_function("regularization_None_create",
                            [POINTER(_c_Regularization)])

        # L1
        self._wrap_function("regularization_L1_create",
                            [POINTER(_c_Regularization), float_ctype])

        # L2
        self._wrap_function("regularization_L2_create",
                            [POINTER(_c_Regularization), float_ctype])

        # VectorUtilities
        self._wrap_function("vector_create_float",
                            [POINTER(POINTER(float_ctype)), uint_ctype])
        
        self._wrap_function("vector_copy_float",
                            [POINTER(float_ctype), POINTER(float_ctype), uint_ctype])

        self._wrap_function("vector_create_uint",
                            [POINTER(POINTER(uint_ctype)), uint_ctype])

        self._wrap_function("vector_copy_uint",
                            [POINTER(uint_ctype), POINTER(uint_ctype), uint_ctype])

        self._wrap_function("matrix2d_float_create",
                            [POINTER(POINTER(_c_Matrix2d_float)), uint_ctype, uint_ctype])

        self._wrap_function("matrix3d_float_create",
                            [POINTER(POINTER(_c_Matrix3d_float)), uint_ctype, uint_ctype, uint_ctype])

        self._wrap_function("matrix4d_float_create",
                            [POINTER(POINTER(_c_Matrix4d_float)), uint_ctype, uint_ctype, uint_ctype, uint_ctype])

        self._wrap_function("matrix5d_float_create",
                            [POINTER(POINTER(_c_Matrix5d_float)), uint_ctype, uint_ctype, uint_ctype, uint_ctype, uint_ctype])

        self._wrap_function("vector_destroy_float",
                            [POINTER(float_ctype)])
        
        self._wrap_function("vector_destroy_uint",
                            [POINTER(uint_ctype)])

        self._wrap_function("matrix2d_float_destroy",
                            [POINTER(_c_Matrix2d_float)])

        self._wrap_function("matrix3d_float_destroy",
                            [POINTER(_c_Matrix3d_float)])

        self._wrap_function("matrix4d_float_destroy",
                            [POINTER(_c_Matrix4d_float)])

        self._wrap_function("matrix5d_float_destroy",
                            [POINTER(_c_Matrix5d_float)])

        # Callbacks
        self._wrap_function("mean_squared_error",
                            [POINTER(float_ctype), POINTER(float_ctype), uint_ctype, POINTER(float_ctype), c_void_p])

        self._wrap_function("mean_squared_error_derivative",
                            [POINTER(float_ctype), POINTER(float_ctype), uint_ctype, POINTER(float_ctype), c_void_p])

        self._wrap_function("sigmoid_dot_product",
                            [POINTER(float_ctype), uint_ctype, POINTER(float_ctype), uint_ctype, POINTER(float_ctype), uint_ctype, uint_ctype, c_void_p])

        self._wrap_function("sigmoid_dot_product_derivative",
                            [POINTER(float_ctype), uint_ctype, POINTER(float_ctype), uint_ctype, POINTER(float_ctype), uint_ctype, uint_ctype, c_void_p])

        self._wrap_function("softmax_dotproduct_3d",
                            [POINTER(float_ctype), uint_ctype, POINTER(float_ctype), uint_ctype, POINTER(float_ctype), uint_ctype, uint_ctype, uint_ctype, c_void_p])

        self._wrap_function("softmax_dotproduct_3d_derivative",
                            [POINTER(float_ctype), uint_ctype, POINTER(float_ctype), uint_ctype, POINTER(_c_Matrix2d_float), uint_ctype, uint_ctype, uint_ctype, c_void_p])

        # RandomLightLabyrinth
        self._wrap_function("reflective_dict_create",
            [POINTER(POINTER(_c_ReflectiveDict)), uint_ctype, uint_ctype, uint_ctype])

        self._wrap_function("reflective_dict_random_create_with_bias",
            [POINTER(POINTER(_c_ReflectiveDict)), uint_ctype, uint_ctype, uint_ctype, uint_ctype, _c_Lcg])

        self._wrap_function("reflective_dict_random_create",
            [POINTER(POINTER(_c_ReflectiveDict)), uint_ctype, uint_ctype, uint_ctype, uint_ctype, _c_Lcg])

        self._wrap_function("reflective_dict_destroy",
            [POINTER(_c_ReflectiveDict)])

        self._wrap_function("reflective_dict_get_ind",
            [POINTER(_c_ReflectiveDict), uint_ctype, uint_ctype, uint_ctype, POINTER(uint_ctype)])

        # RandomLightLabyrinth3D
        self._wrap_function("reflective_dict_3d_create",
            [POINTER(POINTER(_c_ReflectiveDict_3d)), uint_ctype, uint_ctype, uint_ctype, uint_ctype])

        self._wrap_function("reflective_dict_3d_random_create_with_bias",
            [POINTER(POINTER(_c_ReflectiveDict_3d)), uint_ctype, uint_ctype, uint_ctype, uint_ctype, uint_ctype, _c_Lcg])

        self._wrap_function("reflective_dict_3d_random_create",
            [POINTER(POINTER(_c_ReflectiveDict_3d)), uint_ctype, uint_ctype, uint_ctype, uint_ctype, uint_ctype, _c_Lcg])

        self._wrap_function("reflective_dict_3d_destroy",
            [POINTER(_c_ReflectiveDict_3d)])

        self._wrap_function("reflective_dict_3d_get_ind",
            [POINTER(_c_ReflectiveDict_3d), uint_ctype, uint_ctype, uint_ctype, uint_ctype, POINTER(uint_ctype)])

        # Utils
        self._wrap_function("set_random_state",
            [uint_ctype])

        # Lcg
        self._wrap_function("lcg_create",
            [c_uint32], _c_Lcg)

        self._wrap_function("lcg_rand",
            [_c_Lcg], c_uint32)

        self._wrap_function("lcg_split",
            [_c_Lcg], _c_Lcg)

        self._wrap_function("lcg_destroy",
            [_c_Lcg], None)

        # Precompiled
        self._wrap_function("light_labyrinth_full_Gradient_Descent_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Gradient_Descent_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_RMSprop_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Adam_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_full_Nadam_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Gradient_Descent_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_RMSprop_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Adam_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_full_Nadam_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_None_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_L1_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_L2_softmax_dotproduct_3d_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_None_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_L1_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_L2_softmax_dotproduct_3d_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Gradient_Descent_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_RMSprop_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Adam_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_None_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_L1_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_3d_multilabel_Nadam_L2_softmax_dotproduct_3d_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_None_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_L1_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_L2_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_None_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_L1_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_L2_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_None_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_L1_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_L2_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_None_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_L1_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_L2_random_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_None_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_L1_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_L2_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_None_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_L1_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_L2_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_None_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_L1_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_L2_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_None_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_L1_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_L2_random_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_None_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_L1_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Gradient_Descent_L2_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_None_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_L1_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_RMSprop_L2_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_None_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_L1_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Adam_L2_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_None_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_L1_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_full_Nadam_L2_random_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict), 
            POINTER(_c_LearningProcess),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Gradient_Descent_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_RMSprop_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Adam_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_full_Nadam_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_None_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_L1_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_L2_random_3d_softmax_dotproduct_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_None_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_L1_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_L2_random_3d_softmax_dotproduct_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Gradient_Descent_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_RMSprop_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Adam_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_None_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_L1_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("random_light_labyrinth_3d_multilabel_Nadam_L2_random_3d_softmax_dotproduct_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth_3d)),
            POINTER(_c_Matrix4d_float),
            uint_ctype, uint_ctype, uint_ctype, uint_ctype, c_bool, POINTER(_c_ReflectiveDict_3d), 
            POINTER(_c_LearningProcess_3d),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_None_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_L1_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_L2_sigmoid_dot_product_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_None_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_L1_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_L2_sigmoid_dot_product_cross_entropy_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Gradient_Descent_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_RMSprop_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Adam_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_None_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_L1_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])

        self._wrap_function("light_labyrinth_dynamic_full_Nadam_L2_sigmoid_dot_product_scaled_mean_squared_error_fit",
            [POINTER(POINTER(_c_LightLabyrinth)),
            POINTER(_c_Matrix3d_float),
            uint_ctype, uint_ctype, 
            POINTER(_c_LearningProcess_dynamic),
            float_ctype, float_ctype, float_ctype, float_ctype, 
            float_ctype,
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            POINTER(_c_Dataset), POINTER(_c_Dataset),
            uint_ctype, uint_ctype, float_ctype, uint_ctype, uint_ctype, enum_ctype, c_uint32])


    def _wrap_function(self, fun, args, res_type=enum_ctype):
        func = self.dll.__getattr__(fun)
        func.restype = res_type
        func.argtypes = args
        self.__setattr__(fun, func)
        return func

    def _cast_to_c(self, numpy_array):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            if numpy_array is None:
                return None
            shape = numpy_array.shape
            dims = len(shape)
            shape_c = [uint_ctype(x) for x in shape]
            if dims == 1 and issubclass(numpy_array.dtype.type. np.integer):
                c_mat = POINTER(uint_ctype)()
                numpy_array = numpy_array.astype(dtype=uint_dtype, order='C')
                return numpy_array.ctypes.data_as(POINTER(uint_ctype))
            else:
                numpy_array = numpy_array.astype(dtype=float_dtype, order='C')
                if dims == 1:
                    return numpy_array.ctypes.data_as(POINTER(float_ctype))
                elif dims == 2:
                    c_mat = POINTER(_c_Matrix2d_float)()
                    err = self.matrix2d_float_create(byref(c_mat), *shape_c)
                    del_func = self.matrix2d_float_destroy
                    ptr = c_mat.contents.array
                elif dims == 3:
                    c_mat = POINTER(_c_Matrix3d_float)()
                    err = self.matrix3d_float_create(byref(c_mat), *shape_c)
                    del_func = self.matrix3d_float_destroy
                    ptr = c_mat.contents.array
                elif dims == 4:
                    c_mat = POINTER(_c_Matrix4d_float)()
                    err = self.matrix4d_float_create(byref(c_mat), *shape_c)
                    del_func = self.matrix4d_float_destroy
                    ptr = c_mat.contents.array
                elif dims == 5:
                    c_mat = POINTER(_c_Matrix5d_float)()
                    err = self.matrix5d_float_create(byref(c_mat), *shape_c)
                    del_func = self.matrix5d_float_destroy
                    ptr = c_mat.contents.array
                else:
                    raise LightLabyrinthException(
                        f"No cast to C available with {dims} dims (shape {shape})", LightLabyrinthError.INVALID_ARGUMENT)
                if LightLabyrinthError(err) == LightLabyrinthError.NONE:
                    ptr.__del__ = del_func
                    err = self.vector_copy_float(ptr, numpy_array.ctypes.data_as(POINTER(float_ctype)), uint_ctype(math.prod(shape)))
            err = LightLabyrinthError(err)
            if err != LightLabyrinthError.NONE:
                raise LightLabyrinthException(
                    f"Failed to create C array", error=err)

            return c_mat

    def _cast_to_numpy(self, c_matrix, size=None):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", category=RuntimeWarning)
            if c_matrix is None:
                return None
            if isinstance(c_matrix, POINTER(uint_ctype)):
                if size is None:
                    raise LightLabyrinthException(
                        "Size wasn't provided for one dimensional vector", LightLabyrinthError.INVALID_ARGUMENT)
                shape = tuple([size])
                c_array = c_matrix
            elif isinstance(c_matrix, POINTER(float_ctype)):
                if size is None:
                    raise LightLabyrinthException(
                        "Size wasn't provided for one dimensional vector", LightLabyrinthError.INVALID_ARGUMENT)
                shape = tuple([size])
                c_array = c_matrix
            elif isinstance(c_matrix, POINTER(_c_Matrix2d_float)):
                shape = tuple([c_matrix.contents.height, c_matrix.contents.width])
                c_array = c_matrix.contents.array
            elif isinstance(c_matrix, POINTER(_c_Matrix3d_float)):
                shape = tuple(
                    [c_matrix.contents.height, c_matrix.contents.width, c_matrix.contents.inner_size])
                c_array = c_matrix.contents.array
            elif isinstance(c_matrix, POINTER(_c_Matrix4d_float)):
                shape = tuple([c_matrix.contents.height, c_matrix.contents.width,
                            c_matrix.contents.inner_height, c_matrix.contents.inner_width])
                c_array = c_matrix.contents.array
            elif isinstance(c_matrix, POINTER(_c_Matrix5d_float)):
                shape = tuple(c_matrix.contents.dims)
                c_array = c_matrix.contents.array
            else:
                raise LightLabyrinthException(
                    "Unknown type of c_matrix - casting impossible", LightLabyrinthError.INVALID_ARGUMENT)
            if not c_matrix:
                return None
            return np.ctypeslib.as_array(c_array, shape=shape).copy()
    
    def _reflective_dict_to_numpy(self, rdict):
        return self._cast_to_numpy(rdict.contents.indices, size=rdict.contents.total_size).reshape((rdict.contents.height, rdict.contents.width, rdict.contents.mirror_len))

    def _numpy_to_reflective_dict(self, numpy_array):
        if not issubclass(numpy_array.dtype.type, np.integer):
            raise LightLabyrinthException("Numpy array doesn't contain integers")
        if len(numpy_array.shape) != 3:
            raise LightLabyrinthException(f"Numpy array has shape of {numpy_array.shape} but should have 3 dimensions")
        numpy_array = numpy_array.astype(dtype=uint_dtype, order='C')
        rdict = POINTER(_c_ReflectiveDict)()
        err = self.reflective_dict_create(byref(rdict), *numpy_array.shape)
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to create reflective dict", error=err)
        err = self.vector_copy_uint(rdict.contents.indices, numpy_array.ctypes.data_as(POINTER(uint_ctype)), math.prod(numpy_array.shape))
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to copy values to reflective dict", error=err)
        return rdict

    def _reflective_dict_3d_to_numpy(self, rdict):
        return self._cast_to_numpy(rdict.contents.indices, size=rdict.contents.total_size).reshape((rdict.contents.height, rdict.contents.width, rdict.contents.depth, rdict.contents.mirror_len))

    def _numpy_to_reflective_dict_3d(self, numpy_array):
        if not issubclass(numpy_array.dtype.type, np.integer):
            raise LightLabyrinthException("Numpy array doesn't contain integers")
        if len(numpy_array.shape) != 4:
            raise LightLabyrinthException(f"Numpy array has shape of {numpy_array.shape} but should have 4 dimensions")
        numpy_array = numpy_array.astype(dtype=uint_dtype, order='C')
        rdict = POINTER(_c_ReflectiveDict_3d)()
        err = self.reflective_dict_3d_create(byref(rdict), *numpy_array.shape)
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to create reflective dict 3d", error=err)
        err = self.vector_copy_uint(rdict.contents.indices, numpy_array.ctypes.data_as(POINTER(uint_ctype)), math.prod(numpy_array.shape))
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to copy values to reflective dict 3d", error=err)
        return rdict

    def _set_random_state(self, seed):
        err = self.set_random_state(seed)
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException(
                f"Failed to set random state {seed}", error=err)

def check_if_any_exists(paths: List[str]) -> Optional[str]:
    for path in paths:
        if os.path.exists(path):
            return path
    return None

def _get_lib_path():
    ext = get_dll_ext()
    release_name = f"light_labyrinth.{ext}"
    debug_name = f"light_labyrinth_debug.{ext}"
    if _package:
        paths = [
            os.path.join(os.path.dirname(sys.modules["light_labyrinth._light_labyrinth_c"].__file__), debug_name),
            os.path.join(os.path.dirname(sys.modules["light_labyrinth._light_labyrinth_c"].__file__), release_name)
        ]
    else:
        paths = [
            os.path.join(pathlib.Path(__file__).parent.resolve(), debug_name),
            debug_name,
            os.path.join(pathlib.Path(__file__).parent.resolve(), release_name),
            release_name
        ]
    lib_path = check_if_any_exists(paths)
    print(f"Is package: {_package}\n Searching paths: {paths}\nLib path: {lib_path}")

    if lib_path is None:
        paths_str = ', '.join(paths)
        raise LightLabyrinthException(f"None of the {paths_str} exist")
    return lib_path

_libwrapper = _LightLabyrinthLibWrapper(_get_lib_path())

class _LightLabyrinthDataset:
    def __init__(self, numpy_array, add_bias=False):
        self.add_bias = add_bias
        self._c_dataset = POINTER(_c_Dataset)()
        if len(numpy_array.shape) != 2:
            raise LightLabyrinthException(f"Incorrect dimension of numpy_array ({len(numpy_array.shape)}, {numpy_array.shape}), expected 2",
                                      LightLabyrinthError.INVALID_DIMENSION)
        if add_bias:
            numpy_array = np.hstack(
                (numpy_array, np.ones((numpy_array.shape[0], 1))))
        self._height, self._width = numpy_array.shape
        numpy_array = numpy_array.astype(float_dtype, order='C')
        numpy_array_data = numpy_array.ctypes.data_as(POINTER(float_ctype))
        err = _libwrapper.dataset_create_from_1d_array(
            byref(self._c_dataset), numpy_array_data, *numpy_array.shape)
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException("Failed to init dataset", err)

    def as_numpy(self):
        data = POINTER(float_ctype)()
        size = uint_ctype(0)
        err = _libwrapper.dataset_get_data(
            self._c_dataset, byref(data), byref(size))
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException("Failed to get data of dataset", err)
        return np.ctypeslib.as_array(data, shape=(self._height, self._width)).copy()

    def __del__(self):
        err = _libwrapper.dataset_destroy(self._c_dataset)
        err = LightLabyrinthError(err)
        if err != LightLabyrinthError.NONE:
            raise LightLabyrinthException("Failed to destroy dataset", err)