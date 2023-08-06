from enum import Enum


class _LearningProcessBase:
    def __init__(self, name, class_type, destroy_func_name):
        self._name = name
        self._class_type = class_type
        self._destroy_func_name = destroy_func_name

    @property
    def name(self):
        return self._name

    @property
    def class_type(self):
        return self._class_type

    @property
    def destroy_func_name(self):
        return self._destroy_func_name


class LearningProcess(_LearningProcessBase):
    def __init__(self):
        super().__init__("full", "_c_LearningProcess", "free_learning_process")


class LearningProcess3D(_LearningProcessBase):
    class ProcessType(Enum):
        full = 1
        multilabel = 2
        mixed = 3

    def __init__(self, process_type):
        super().__init__(process_type.name, "_c_LearningProcess_3d", "free_learning_process_3d")


class LearningProcessDynamic(_LearningProcessBase):
    def __init__(self, ):
        super().__init__("full", "_c_LearningProcess_dynamic", "free_learning_process_dynamic")
