"""Stamox: Stats Models in JAX Library"""

import sys

from stamox import anova
from stamox import cluster
from stamox import distribution
from stamox import hypothesis
from stamox import math
from stamox import maps
from stamox import core
from stamox import basic
from stamox import regression
from stamox import decomposition
from stamox import sample


_REQUIRED_JAX_VERSION = "0.3.23"  # pylint: disable=g-statement-before-imports


def _check_py_version():
    if sys.version_info[0] < 3:
        raise Exception("Please use Python 3. Python 2 is not supported.")


# make sure jax is installed
# def _ensure_jax_install():
#     """Attempt to import JAX, and make sure its version is sufficient.
#     Raises:
#         ImportError: if either JAX is not importable or its version is
#         inadequate.
#     """
#     try:
#         import jax
#     except ImportError:
#         # Print more informative error message, then reraise.
#         print("\n\nFailed to import JAX. Please note that JAX is not "
#             "installed by default when you install JAX Quant Finance library. "
#             "This is so that users can decide whether to install the GPU/TPU-enabled "
#             "JAX package. To use STAMOX library, please install "
#             "the most recent version of JAX, by following instructions at "
#             "https://github.com/google/jax#installation.\n\n")
#         raise

#     import distutils.version

#     if (distutils.version.LooseVersion(jax.__version__) <
#         distutils.version.LooseVersion(_REQUIRED_JAX_VERSION)):
#         raise ImportError(
#             "This version of STAMOX requires JAX "
#             "version >= {required}; Detected an installation of version {present}. "
#             "Please upgrade JAX to proceed.".format(
#                 required=_REQUIRED_JAX_VERSION, present=jax.__version__))

_check_py_version()
# _ensure_jax_install()


__all__ = [
    "anova",
    "cluster",
    "distribution",
    "hypothesis",
    "math",
    "maps",
    "core",
    "basic",
    "regression",
    "decomposition",
    "sample",
]
