from typing import Union, Optional

import jax.numpy as jnp
import jax.random as jrand
from jax.random import KeyArray
from jax._src.random import Shape
from equinox import filter_jit, filter_grad, filter_vmap
from jaxtyping import ArrayLike, Float, Array, Bool

from ..core import make_partial_pipe


@filter_jit
def _pcauchy(
    x: Union[Float, ArrayLike],
    loc: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
) -> Array:
    scaled = (x - loc) / scale
    return jnp.arctan(scaled) / jnp.pi + 0.5


@make_partial_pipe
def pcauchy(
    x: Union[Float, ArrayLike],
    loc: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: Bool = True,
    log_prob: Bool = False,
) -> Array:
    """Calculates the cumulative denisty probability c function of the Cauchy distribution.

    Args:
        x (Union[Float, ArrayLike]): The value at which to evaluate the PDF.
        loc (Union[Float, ArrayLike], optional): The location parameter of the Cauchy distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter of the Cauchy distribution. Defaults to 1.0.
        lower_tail (Bool, optional): Whether to return the lower tail probability. Defaults to True.
        log_prob (Bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        Array: The cumulative density function of the Cauchy distribution.
    """
    x = jnp.atleast_1d(x)
    p = filter_vmap(_pcauchy)(x, loc, scale)
    if not lower_tail:
        p = 1 - p
    if log_prob:
        p = jnp.log(p)
    return p


_dcauchy = filter_grad(filter_jit(_pcauchy))


@make_partial_pipe
def dcauchy(
    x: Union[Float, ArrayLike],
    loc: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: Bool = True,
    log_prob: Bool = False,
) -> Array:
    """Computes the pdf of the Cauchy distribution.

    Args:
        x (Union[Float, ArrayLike]): The input values.
        loc (Union[Float, ArrayLike], optional): The location parameter. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter. Defaults to 1.0.
        lower_tail (Bool, optional): Whether to compute the lower tail. Defaults to True.
        log_prob (Bool, optional): Whether to compute the log probability. Defaults to False.

    Returns:
        Array: The pdf of the Cauchy distribution.
    """
    x = jnp.atleast_1d(x)
    grads = filter_vmap(_dcauchy)(x, loc, scale)
    if not lower_tail:
        grads = 1 - grads
    if log_prob:
        grads = jnp.log(grads)
    return grads


@filter_jit
def _qcauchy(
    q: Union[Float, ArrayLike],
    loc: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
):
    return loc + scale * jnp.tan(jnp.pi * (q - 0.5))


@make_partial_pipe
def qcauchy(
    q: Union[Float, ArrayLike],
    loc: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: Bool = True,
    log_prob: Bool = False,
) -> Array:
    """Computes the quantile of the Cauchy distribution.

    Args:
        q (Union[Float, ArrayLike]): Quantiles to compute.
        loc (Union[Float, ArrayLike], optional): Location parameter. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): Scale parameter. Defaults to 1.0.
        lower_tail (Bool, optional): Whether to compute the lower tail. Defaults to True.
        log_prob (Bool, optional): Whether to compute the log probability. Defaults to False.

    Returns:
        Array: The quantiles of the Cauchy distribution.
    """
    q = jnp.atleast_1d(q)
    if not lower_tail:
        q = 1 - q
    if log_prob:
        q = jnp.exp(q)
    return filter_vmap(_qcauchy)(q, loc, scale)


def _rcauchy(
    key: KeyArray,
    loc: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    sample_shape: Optional[Shape] = None,
):
    if sample_shape is None:
        sample_shape = jnp.broadcast_shapes(jnp.shape(loc), jnp.shape(scale))
    loc = jnp.broadcast_to(loc, sample_shape)
    scale = jnp.broadcast_to(scale, sample_shape)
    return jrand.cauchy(key, sample_shape) * scale + loc


@make_partial_pipe
def rcauchy(
    key: KeyArray,
    loc: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    sample_shape: Optional[Shape] = None,
    lower_tail: Bool = True,
    log_prob: Bool = False,
) -> Array:
    """Generates random samples from the Cauchy distribution.

    Args:
        key: A PRNGKey to use for generating the samples.
        loc: The location parameter of the Cauchy distribution.
        scale: The scale parameter of the Cauchy distribution.
        sample_shape: The shape of the output array.
        lower_tail: Whether to return the lower tail probability.
        log_prob: Whether to return the log probability.

    Returns:
        An array of samples from the Cauchy distribution.
    """
    probs = _rcauchy(key, loc, scale, sample_shape)
    if not lower_tail:
        probs = 1 - probs
    if log_prob:
        probs = jnp.log(probs)
    return probs
