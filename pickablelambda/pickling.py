import inspect
import pickle
import copyreg
import types

def pickle_lambda_proxy(lambda_proxy):
    pickled_code = lambda_proxy.dumps()
    return unpickle_lambda, (pickled_code,)

def unpickle_lambda(pickled_code):
    lambda_ = LambdaProxy.loads(pickled_code)
    return lambda_


def make_lambda_pickable():
    copyreg.pickle(LambdaProxy, pickle_lambda_proxy)

def is_lambda_function(obj):
    return isinstance(obj, types.LambdaType) and obj.__name__ == "<lambda>"

def pickable(lambda_):
    return LambdaProxy(lambda_) if is_lambda_function(lambda_) else lambda_


class LambdaProxy():
    def __init__(self, lambda_):
        self._lambda_code = LambdaProxy.lambda2str(lambda_)
        self._lambda = None

    def dumps(self):
        return pickle.dumps(self._lambda_code)

    @classmethod
    def loads(cls, pickled_code):
        lambda_code = pickle.loads(pickled_code)
        lambda_ = cls.str2lambda(lambda_code)
        if isinstance(lambda_, types.FunctionType):
            return lambda_
        else:
            raise Exception("Looking for lambda in pickled object, but found " + str(type(lambda_)))

    @staticmethod
    def lambda2str(lambda_):
        arguments = ",".join(inspect.signature(lambda_).parameters)
        source_code = inspect.getsource(lambda_).split(":")[1].strip()
        return "lambda " + arguments + ": " + source_code

    @staticmethod
    def str2lambda(lambda_code):
        return eval(lambda_code)

    def __call__(self, *args):
        if self._lambda is  None:
            self._lambda = LambdaProxy.str2lambda(self._lambda_code)
        return self._lambda(*args)

    def lambda_(self):
        if self._lambda is  None:
            self._lambda = LambdaProxy.str2lambda(self._lambda_code)
        return self._lambda

make_lambda_pickable()


