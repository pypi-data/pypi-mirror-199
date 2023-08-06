from typing import Union, Optional

import jax.random as jrand
import jax.numpy as jnp
from jax._src.random import KeyArray, Shape
from jaxtyping import ArrayLike, Float, Array
from equinox import filter_jit, filter_vmap, filter_grad

from ..core import make_partial_pipe


@filter_jit
def _pweibull(
    x: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
) -> Array:
    return 1 - jnp.exp(-((x / scale) ** concentration))


@make_partial_pipe
def pweibull(
    x: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: bool = True,
    log_prob: bool = False,
) -> Array:
    """Computes the cumulative distribution function of the Weibull distribution.

    Args:
        x (Union[Float, ArrayLike]): The value at which to evaluate the CDF.
        concentration (Union[Float, ArrayLike], optional): The concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter of the Weibull distribution. Defaults to 1.0.
        lower_tail (bool, optional): Whether to compute the lower tail of the CDF. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        Array: The cumulative distribution function of the Weibull distribution evaluated at `x`.
    """
    x = jnp.atleast_1d(x)
    p = filter_vmap(_pweibull)(x, concentration, scale)
    if not lower_tail:
        p = 1 - p
    if log_prob:
        p = jnp.log(p)
    return p


_dweibull = filter_grad(filter_jit(_pweibull))


@make_partial_pipe
def dweibull(x, concentration=0.0, scale=1.0, lower_tail=True, log_prob=False):
    """Computes the probability density function of the Weibull distribution.

    Args:
        x (Union[Float, ArrayLike]): The value at which to evaluate the PDF.
        concentration (Union[Float, ArrayLike], optional): The concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter of the Weibull distribution. Defaults to 1.0.
        lower_tail (bool, optional): Whether to compute the lower tail of the CDF. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        Array: The probability density function of the Weibull distribution evaluated at `x`.
    """
    x = jnp.atleast_1d(x)
    grads = filter_vmap(_dweibull)(x, concentration, scale)
    if not lower_tail:
        grads = 1 - grads
    if log_prob:
        grads = jnp.log(grads)
    return grads


@filter_jit
def _qweibull(
    q: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
) -> Array:
    x = jnp.float_power(-jnp.log(1 - q), 1 / concentration) * scale
    return x


@make_partial_pipe
def qweibull(
    q: Union[Float, ArrayLike],
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    lower_tail: bool = True,
    log_prob: bool = False,
) -> Array:
    """Computes the quantile function of the Weibull distribution.

    Args:
        q (Union[Float, ArrayLike]): The quantiles to compute.
        concentration (Union[Float, ArrayLike], optional): The concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): The scale parameter of the Weibull distribution. Defaults to 1.0.
        lower_tail (bool, optional): Whether to compute the lower tail of the distribution. Defaults to True.
        log_prob (bool, optional): Whether to compute the log probability of the distribution. Defaults to False.

    Returns:
        Array: The computed quantiles.
    """
    q = jnp.atleast_1d(q)
    if not lower_tail:
        q = 1 - q
    if log_prob:
        q = jnp.exp(q)
    x = filter_vmap(_qweibull)(q, concentration, scale)
    return x


@filter_jit
def _rweibull(
    key: KeyArray,
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    sample_shape: Optional[Shape] = None,
):
    return jrand.weibull_min(key, scale, concentration, sample_shape)


@make_partial_pipe
def rweibull(
    key: KeyArray,
    concentration: Union[Float, ArrayLike] = 0.0,
    scale: Union[Float, ArrayLike] = 1.0,
    sample_shape: Optional[Shape] = None,
    lower_tail: bool = True,
    log_prob: bool = False,
):
    """Generates samples from the Weibull distribution.

    Args:
        key (KeyArray): Random key used for generating random numbers.
        concentration (Union[Float, ArrayLike], optional): Concentration parameter of the Weibull distribution. Defaults to 0.0.
        scale (Union[Float, ArrayLike], optional): Scale parameter of the Weibull distribution. Defaults to 1.0.
        sample_shape (Optional[Shape], optional): Shape of the output sample. Defaults to None.
        lower_tail (bool, optional): Whether to return the lower tail probability. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        probs (float): Probability of the Weibull distribution.
    """
    probs = _rweibull(key, concentration, scale, sample_shape)
    if not lower_tail:
        probs = 1 - probs
    if log_prob:
        probs = jnp.log(probs)
    return probs
