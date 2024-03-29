import inspect
import functools
import numpy as np
import math


__all__ = ['Abs', 'Loge', 'Log2', 'Log10', 'Exp',
            'Power2', 'Power3', 'Power4', 'Sqrt', 'Inv', 'InvPower2']


class BaseTransformer:
    """ The base class for transforming a data series, the __call__ method needs to be 
        implemented in subclasses.

        Each transformation has a complexity score, when multiple transformations yield
        the same amount of improvement, the one with the lowest complexity will be picked.
    """
    complexity = None
        
    def __init__(self):
        self.params = None

    def __repr__(self):
        return 'Transform<{}:{}>'.format(self.__class__.__name__, self.params)
        
    def __call__(self, x):
        return NotImplementedError

    def validate_input(self, x):
        """ Overwrite this method to validate the input before fitting parameters 
            return whether `x` is valid for the current transformation
        """
        return np.isfinite(x).all()
    
    def get_params(self):
        """ Return the variable name for the parameters """
        sig = inspect.signature(self.__call__)
        params = [k for k in sig.parameters if k != 'x']
        return params
    
    def set_params(self, params=None, **kwargs):
        """ Accept both passing parameters as a dictionary and keyword arguments"""
        self.params = params if params is not None else kwargs
        
    def transform(self, x):
        if self.params is None:
            raise ValueError('No parameter values, call the set_params method first with the fitted parameter value.')
        fn = functools.partial(self.__call__, **self.params)
        return fn(x)


class Abs(BaseTransformer):
    complexity = 50

    def __call__(self, x, a, b):
        return np.abs(a * x + b)


class Loge(BaseTransformer):
    complexity = 26

    def __call__(self, x, a, b):
        return np.log(a * x + b)


class Log2(BaseTransformer):
    complexity = 25
    
    def __call__(self, x, a, b):
        return np.log2(a * x + b)


class Log10(BaseTransformer):
    complexity = 35

    def __call__(self, x, a, b):
        return np.log10(a * x + b)


class Exp(BaseTransformer):
    complexity = 40

    def __call__(self, x, a, b):
        return np.exp(a * x + b)


class _Power(BaseTransformer):
    n = 1
    complexity = n * 30

    def __call__(self, x, a, b):
        if self.n > 0:
            return np.power(a * x + b, self.n)
        else:
            return 1 / (np.power(a * x + b, -self.n) + 1e-15)


class Power2(_Power):
    n = 2


class Power3(_Power):
    n = 3


class Power4(_Power):
    n = 4


class Sqrt(_Power):
    n = 1 / 2
    complexity = 33


class Inv(_Power):
    n = -1
    complexity = 37


class InvPower2(_Power):
    n = -2
    complexity = 67


# DEFAULT_TRANSFORM = [Abs, Loge, Exp, Power2, Power3, Sqrt, Inv, InvPower2]
DEFAULT_TRANSFORM = [Loge, Exp, Power2, Sqrt, Inv]
