from typing import Union, Optional

import jax.random as jrand
import jax.numpy as jnp
from jax._src.random import KeyArray, Shape
from jaxtyping import ArrayLike, Float, Array
from equinox import filter_jit, filter_vmap, filter_grad

from ..math.special import fdtri, fdtr
from ..core import make_partial_pipe


@filter_jit
def _pf(
    x: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
):
    return fdtr(dfn, dfd, x)


@make_partial_pipe
def pF(
    x: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    lower_tail=True,
    log_prob=False,
):
    """Calculates the cumulative distribution function of the F-distribution.

    Args:
        x (Union[Float, ArrayLike]): The value at which to evaluate the cdf.
        dfn (Union[Float, ArrayLike]): The numerator degrees of freedom.
        dfd (Union[Float, ArrayLike]): The denominator degrees of freedom.
        lower_tail (bool, optional): If True (default), the lower tail probability is returned.
        log_prob (bool, optional): If True, the logarithm of the probability is returned.

    Returns:
        float or array_like: The cumulative distribution function evaluated at `x`.
    """
    x = jnp.atleast_1d(x)
    p = filter_vmap(_pf)(x, dfn, dfd)
    if not lower_tail:
        p = 1 - p
    if log_prob:
        p = jnp.log(p)
    return p


_df = filter_jit(filter_grad(_pf))


@make_partial_pipe
def dF(
    x: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    lower_tail=True,
    log_prob=False,
):
    """Calculates the gradient of the cumulative distribution function for a given x, dfn and dfd.

    Args:
        x (Union[Float, ArrayLike]): The value at which to calculate the gradient of the cumulative distribution function.
        dfn (Union[Float, ArrayLike]): The numerator degrees of freedom.
        dfd (Union[Float, ArrayLike]): The denominator degrees of freedom.
        lower_tail (bool, optional): Whether to calculate the lower tail of the cumulative distribution function. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        grads (float or array): The gradient of the cumulative distribution function.
    """
    x = jnp.atleast_1d(x)
    grads = filter_vmap(_df)(x, dfn, dfd)
    if not lower_tail:
        grads = 1 - grads
    if log_prob:
        grads = jnp.log(grads)
    return grads


@filter_jit
def _qf(
    q: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
):
    return fdtri(dfn, dfd, q)


@make_partial_pipe
def qF(
    q: Union[Float, ArrayLike],
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    lower_tail=True,
    log_prob=False,
) -> Array:
    """Calculates the quantile function of a given distribution.

    Args:
        q (Union[Float, ArrayLike]): The quantile to calculate.
        dfn (Union[Float, ArrayLike]): The degrees of freedom for the numerator.
        dfd (Union[Float, ArrayLike]): The degrees of freedom for the denominator.
        lower_tail (bool, optional): Whether to calculate the lower tail or not. Defaults to True.
        log_prob (bool, optional): Whether to calculate the log probability or not. Defaults to False.

    Returns:
        Array: The calculated quantile.
    """
    q = jnp.atleast_1d(q)
    if not lower_tail:
        q = 1 - q
    if log_prob:
        q = jnp.exp(q)
    return filter_vmap(_qf)(q, dfn, dfd)


@filter_jit
def _rf(
    key: KeyArray,
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    sample_shape: Optional[Shape] = None,
):
    if sample_shape is None:
        sample_shape = jnp.broadcast_shapes(jnp.shape(dfn), jnp.shape(dfd))
    dfn = jnp.broadcast_to(dfn, sample_shape)
    dfd = jnp.broadcast_to(dfd, sample_shape)
    return jrand.f(key, dfn, dfd, shape=sample_shape)


@make_partial_pipe
def rF(
    key: KeyArray,
    dfn: Union[Float, ArrayLike],
    dfd: Union[Float, ArrayLike],
    sample_shape: Optional[Shape] = None,
    lower_tail=True,
    log_prob=False,
):
    """Calculates the probability of a random variable following a F-distribution.

    Args:
        key (KeyArray): Random key used for PRNG.
        dfn (Union[Float, ArrayLike]): Degrees of freedom in numerator.
        dfd (Union[Float, ArrayLike]): Degrees of freedom in denominator.
        sample_shape (Optional[Shape], optional): Shape of the samples to be drawn. Defaults to None.
        lower_tail (bool, optional): Whether to calculate the lower tail probability. Defaults to True.
        log_prob (bool, optional): Whether to return the log probability. Defaults to False.

    Returns:
        probs (float or array): Probability of the random variable following a F-distribution.
    """
    probs = _rf(key, dfn, dfd, sample_shape)
    if not lower_tail:
        probs = 1 - probs
    if log_prob:
        probs = jnp.log(probs)
    return probs
