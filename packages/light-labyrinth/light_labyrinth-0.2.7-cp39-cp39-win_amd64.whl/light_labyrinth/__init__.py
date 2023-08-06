"""
`Light Labyrinth` -- Multipurpose Supervised Machine Learning Models
====================================================================
-----------
**This package includes implementations of the Light Labyrinth models.**

Easy-to-use Python API allows for training powerful machine learning
models within only a few lines of code, while the highly-optimized
core of the library written in C contributes to their high performance 
and efficiency.

Platforms
---------
**Unix**, **Windows**

Authors
-------
**Krzysztof Więcław** <wutus@lightlabyrinth.org>

**Marcin Zakrzewski** <enkar@lightlabyrinth.org>
"""

try:
    from ._version import __version__
    __all__ = ["__version__"]
except ImportError:
    __all__ = []
