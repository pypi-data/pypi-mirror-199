"""
The `light_labyrinth.multioutput` module includes Light Labyrinth models for
multilabel classification, multioutput regression, and mixed output prediction.

All the models are adaptation-based -- rather than transforming data to suit
standard classifiers, the models themselves are adapted to operate on several
output variables at once. This approach is generally more effective than
One-vs-rest as it utilizes correlation between classes and is more practical
than creating a label-powerset that can only be used with a few labels. 

.. include:: ../../html_utils/multilabel.svg
"""

from ._LightLabyrinth3DMultilabelClassifier import LightLabyrinth3DMultilabelClassifier
from ._LightLabyrinth3DMultioutputRegressor import LightLabyrinth3DMultioutputRegressor

from ._LightLabyrinth3DRandomMultilabelClassifier import LightLabyrinth3DRandomMultilabelClassifier
from ._LightLabyrinth3DRandomMultioutputRegressor import LightLabyrinth3DRandomMultioutputRegressor

from ._LightLabyrinth3DMixedOutputPredictor import LightLabyrinth3DMixedOutputPredictor

__all__ = ["LightLabyrinth3DMultilabelClassifier", \
           "LightLabyrinth3DMultioutputRegressor", \
           "LightLabyrinth3DRandomMultilabelClassifier", \
           "LightLabyrinth3DRandomMultioutputRegressor", \
           "LightLabyrinth3DMixedOutputPredictor"]