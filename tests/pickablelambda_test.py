import unittest
import pickle
import types

from pickablelambda import make_lambda_pickable, LambdaProxy

class TestLambdaProxy(unittest.TestCase):

    def test_pickle_lambda_raises_ex(self):
        lmb = lambda x: x+1
        with self.assertRaises(Exception):
            pickle_bin = pickle.dumps(lmb)


    def test_pickle_with_lamdba_proxy(self):
        make_lambda_pickable()
        lmb = lambda x: x+1
        pickle_bin = pickle.dumps(LambdaProxy(lmb))
        lmb2 = pickle.loads(pickle_bin)
        self.assertEqual(lmb(10), lmb2(10))
        self.assertTrue(isinstance(lmb2, types.FunctionType))


    def test_use_lambda_proxy(self):
        make_lambda_pickable()
        lmb = lambda x: x+1
        proxy = LambdaProxy(lmb)
        self.assertEqual(lmb(100), proxy(100))


    def test_use_lambda_proxy_2_args(self):
        make_lambda_pickable()
        lmb = lambda x, y: x+y
        proxy = LambdaProxy(lmb)
        self.assertEqual(lmb(100, 200), proxy(100, 200))

    def test_use_lambda_second_order_equation(self):
        make_lambda_pickable()
        lmb = lambda x: 5*x**2 + 3*x + 4
        proxy = LambdaProxy(lmb)
        self.assertEqual(lmb(2), proxy(2)) #y=30

if __name__ == "__main__":
    unittest.main()