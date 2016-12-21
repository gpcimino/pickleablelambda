import pickle

with open('lambda.pickle', 'rb') as f:
    L = pickle.load(f)
print("found a " + str(type(L)) + " in pickle file, now execute L(10)")
print("L(10)=" + str(L(10)))
print("unpickled object is " + str(type(L)))

from pickablelambda import is_lambda_function
print("check if unpickled object is a lambda: " + str(is_lambda_function(L)))

