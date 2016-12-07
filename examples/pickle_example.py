from pickablelambda import make_lambda_pickable, LambdaProxy
import pickle

L = lambda x: x+1

print("L(10)=" + str(L(10)))

with open('lambda.pickle', 'wb') as f:
    pickle.dump(LambdaProxy(L), f)
