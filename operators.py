import math

import numpy as np
import scipy

from decorators import register, tuplify, protect, memoize_fibonacci


@register
@tuplify
def addition(x: float, y: float) -> float:
    return x + y


@register
@tuplify
def subtraction(x: float, y: float) -> float:
    return x - y


@register
@tuplify
def multiplication(x: float, y: float) -> float:
    return x * y


@register
@protect(nonnan_output=True, integer_output=True)
@tuplify
def division(x: float, y: float) -> float:
    if y == 0.0:
        return np.nan
    return x / y


@register
@protect(nonnan_output=True)
@tuplify
def modulo(x: float, y: float) -> float:
    if y == 0.0:
        return np.nan
    return x % y


@register
@protect(max_input=10, min_input=0, integer_input=True)
@tuplify
def factorial(x: int) -> int:
    return math.factorial(x)


@register
@protect(min_input=0, integer_output=True, max_input=1000000000)
@tuplify
def square_root(x: float) -> float:
    return np.sqrt(x)


@register
@protect(max_input=16)
@tuplify
def binomial_coefficient(n: int, k: int) -> int:
    return scipy.special.comb(n, k, exact=True)


@register
@protect(integer_input=True, max_input=25, min_input=0)
@tuplify
def fibonacci(n: int) -> int:
    return mem_fib(n)


@memoize_fibonacci
def mem_fib(n):
    return mem_fib(n - 1) + mem_fib(n - 2)
