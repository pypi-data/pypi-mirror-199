"""
The `light_labyrinth.hyperparams.regularization` module includes `Regularization` classes
that can be used for training Light Labyrinth models. The regularization term added to the
loss function prevents model from overfitting.
"""

from ._regularization import (RegularizationL1, RegularizationL2,
                              RegularizationNone)

__all__ = ["RegularizationL1", "RegularizationL2", "RegularizationNone"]
