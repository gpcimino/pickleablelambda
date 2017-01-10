"""
Pickleable lambda.

Makes lambda functions pickleable via a proxy class.
"""

import copyreg
import inspect
import pickle
import types


def pickle_lambda_proxy(lambda_proxy):
    """Pickle a lambda proxy."""
    pickled_code = lambda_proxy.dumps()
    return unpickle_lambda, (pickled_code,)


def unpickle_lambda(pickled_code):
    """Unpickle a lambda proxy."""
    lambda_ = LambdaProxy.loads(pickled_code)
    return lambda_


def make_lambda_pickleable():
    """Register class `LambdaProxy` in `copyreg`"""
    copyreg.pickle(LambdaProxy, pickle_lambda_proxy)


def is_lambda_function(obj):
    """Find out of `obj` is a lambda."""
    return isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>"


def pickleable(lambda_):
    """Make a lambda function pickleable."""
    return LambdaProxy(lambda_) if is_lambda_function(lambda_) else lambda_


class LambdaProxy():
    """Proxy for lambda that allows pickling.
    """
    def __init__(self, lambda_):
        self._lambda_code = LambdaProxy.lambda2str(lambda_)
        self._lambda = None

    def dumps(self):
        """Return pickled object as bytes."""
        return pickle.dumps(self._lambda_code)

    @classmethod
    def loads(cls, pickled_code):
        """Unpickle pickled code from bytes."""
        lambda_code = pickle.loads(pickled_code)
        lambda_ = cls.str2lambda(lambda_code)
        if isinstance(lambda_, types.FunctionType):
            return lambda_
        else:
            msg = "Looking for lambda in pickled object, but found {}".format(
                type(lambda_))
            raise Exception(msg)

    @staticmethod
    def lambda2str(lambda_):
        """Convert lambda into a string."""
        arguments = ",".join(inspect.signature(lambda_).parameters)
        source_code = inspect.getsource(lambda_).split(":")[1].strip()
        return "lambda " + arguments + ": " + source_code

    @staticmethod
    def str2lambda(lambda_code):
        """Evaluate code, i.e. turn string with code into a lambda. """
        return eval(lambda_code)  # pylint: disable=eval-used

    def __call__(self, *args):
        if self._lambda is None:
            self._lambda = LambdaProxy.str2lambda(self._lambda_code)
        return self._lambda(*args)

    def lambda_(self):
        """Return lambda proxy."""
        if self._lambda is None:
            self._lambda = LambdaProxy.str2lambda(self._lambda_code)
        return self._lambda


make_lambda_pickleable()
