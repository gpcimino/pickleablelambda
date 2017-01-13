# pylint: disable=missing-docstring, invalid-name, C0301

from functools import partial
import pickle
import unittest
import types


from pickleablelambda import pickleable

def mysum(x, y):
    return x+y

def incr(x):
    return x+1


class TestLambdaProxy(unittest.TestCase):

    def test_pickle_lambda_raises_ex(self):
        lmb = lambda x: x+1
        with self.assertRaises(Exception):
            pickle.dumps(lmb)

    def test_pickle_with_lamdba_proxy(self):
        lmb = lambda x: x+1
        pickle_bin = pickle.dumps(pickleable(lmb))
        lmb2 = pickle.loads(pickle_bin)
        self.assertEqual(lmb(10), lmb2(10))
        self.assertTrue(isinstance(lmb2, types.FunctionType))

    def test_use_lambda_proxy(self):
        lmb = lambda x: x+1
        proxy = pickleable(lmb)
        self.assertEqual(lmb(100), proxy(100))

    def test_use_lambda_proxy_2_args(self):
        lmb = lambda x, y: x+y
        proxy = pickleable(lmb)
        self.assertEqual(lmb(100, 200), proxy(100, 200))

    def test_use_lambda_second_order_equation(self):
        lmb = lambda x: 5*x**2 + 3*x + 4
        proxy = pickleable(lmb)
        self.assertEqual(lmb(2), proxy(2))

    def test_make_func_pickleable_not_raise_err(self):
        proxy = pickleable(incr)
        self.assertEqual(3, proxy(2))

    @staticmethod
    def dummy_func(x):
        return x+1

    def test_make_class_method_pickleable_not_raise_err(self):
        proxy = pickleable(self.dummy_func)
        self.assertEqual(3, proxy(2))

    def test_make_partial_func_pickleable_not_raise_err(self):
        partial_func = partial(incr, x=2)
        proxy = pickleable(partial_func)
        self.assertEqual(3, proxy())

    def test_make_partial_func_2args_pickleable_not_raise_err(self):
        partial_func = partial(mysum, y=2)
        proxy = pickleable(partial_func)
        self.assertEqual(3, proxy(1))

    def test_with_complex_line_in_source_code(self):
        pickled_f1, pickled_f2 = self.dummy_method(pickleable(lambda x: x+1), pickleable(lambda x, y: x+y)) # pylint: disable=line-too-long
        f1 = pickle.loads(pickled_f1)
        f2 = pickle.loads(pickled_f2)

        self.assertEqual(3, f1(2))
        self.assertEqual(5, f2(2, 3))

    def test_with_super_complex_line_in_source_code(self):
        pickled_f1, pickled_f2 = self.dummy_method(pickleable(lambda size: [int(y) for y in [str(x) for x in range(size) if x%2 == 0]]), pickleable(lambda x, y: x+y)) # pylint: disable=line-too-long
        f1 = pickle.loads(pickled_f1)
        f2 = pickle.loads(pickled_f2)

        self.assertEqual([0, 2, 4, 6, 8], f1(9))
        self.assertEqual(5, f2(2, 3))

    def test_with_nested_lambdas(self):
        #wired nested lambda calculus
        pickled_f1, _ = self.dummy_method(pickleable(lambda F, m: lambda x: F(x)*m))
        f1 = pickle.loads(pickled_f1)
        self.assertEqual(12, f1(lambda x: x**2, 3)(2))

    def dummy_method(self, f1, f2=""):
        return pickle.dumps(f1), pickle.dumps(f2)

    #@unittest.skip
    def test_use_func_in_lambda(self):
        print(incr(10))
        pickled_f1, _ = self.dummy_method(pickleable(lambda y: incr(y)))
        f1 = pickle.loads(pickled_f1)
        self.assertEqual(3, f1(2))




if __name__ == "__main__":
    unittest.main()
