"""
Pickleable lambda.

Makes lambda functions pickleable via a proxy class.
"""

import sys 
import pickle

from types import CodeType, LambdaType, FunctionType

if sys.version_info[0] == 3:
    #python 3
    import copyreg
else:
    #python 2
    import copy_reg as copyreg


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
    """Find out if `obj` is a lambda."""
    return isinstance(obj, LambdaType) and obj.__name__ == "<lambda>"


def pickleable(lambda_):
    """Make a lambda function pickleable."""
    return LambdaProxy(lambda_) if is_lambda_function(lambda_) else lambda_


class LambdaProxy(object):
    """Proxy for lambda that allows pickling.
    """
    def __init__(self, lambda_):
        self._lambda_bytecode = LambdaProxy.lambda2bytecode(lambda_) 
        self._lambda = None

    def dumps(self):
        """Return pickled object as bytes."""
        return pickle.dumps(self._lambda_bytecode)

    @classmethod
    def loads(cls, pickled_code):
        """Unpickle pickled code from bytes."""
        lambda_code = pickle.loads(pickled_code)
        lambda_ = cls.bytecode2lambda(lambda_code)
        if isinstance(lambda_, FunctionType):
            return lambda_
        else:
            msg = "Looking for lambda in pickled object, but found {}".format(
                type(lambda_))
            raise Exception(msg)

    @staticmethod
    def lambda2bytecode(lambda_):
        """Convert lambda into a tuple containing the attribute of a Code object."""
        co = lambda_.__code__
        if sys.version_info[0] == 3:
            co_tuple=[co.co_argcount, co.co_kwonlyargcount,
                co.co_nlocals, co.co_stacksize, co.co_flags,
                co.co_code, co.co_consts, co.co_names,
                co.co_varnames, co.co_filename,
                lambda_.__name__,
                co.co_firstlineno, co.co_lnotab, co.co_freevars,
                co.co_cellvars]
        else:
            co_tuple=[co.co_argcount, #co.co_kwonlyargcount,
                co.co_nlocals, co.co_stacksize, co.co_flags,
                co.co_code, co.co_consts, co.co_names,
                co.co_varnames, co.co_filename,
                lambda_.__name__,
                co.co_firstlineno, co.co_lnotab, co.co_freevars,
                co.co_cellvars]
        return co_tuple


    @staticmethod
    def bytecode2lambda(r):
        """Instanciate a Code object containing a lambda in a lambda object. """
        if sys.version_info[0] == 3:
            deserialized_code_obj = CodeType(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13], r[14])
        else:
            deserialized_code_obj = CodeType(r[0],r[1],r[2],r[3],r[4],r[5],r[6],r[7],r[8],r[9],r[10],r[11],r[12],r[13]) 
        fake = lambda x : x
        fake.__code__ = deserialized_code_obj        
        return fake

    def __call__(self, *args):
        if self._lambda is None:
            self._lambda = LambdaProxy.bytecode2lambda(self._lambda_bytecode)
        return self._lambda(*args)

    def lambda_(self):
        """Return lambda proxy."""
        if self._lambda is None:
            self._lambda = LambdaProxy.bytecode2lambda(self._lambda_bytecode)
        return self._lambda


make_lambda_pickleable()
