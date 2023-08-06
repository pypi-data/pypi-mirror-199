"""
The `light_labyrinth.sklearn_wrappers` module includes wrapper classes which allow
to treat Light Labyrinth models as Scikit-learn estimators.
"""

from ._SklearnClassifierWrapper import SklearnClassifierWrapperModel
from ._SklearnRegressorWrapper import SklearnRegressorWrapperModel

__all__ = ["SklearnClassifierWrapperModel", "SklearnRegressorWrapperModel"]
