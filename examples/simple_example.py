from pickablelambda import make_lambda_pickable, LambdaProxy
import pickle

print("Define L = lambda x: x+1")
L = lambda x: x+1

print("Execute lambda")
print("L(10)=" + str(L(10)))


print("Try to pickle lambda...")
try:
    with open('lambda.pickle', 'wb') as f:
        pickle.dump(L, f)    
except:
    print(".. unfortunately lambdas are not picklable :-(")

print("But if you call make_lambda_pickable() once and you wrap L with LambdaProxy...")
make_lambda_pickable()

with open('lambda.pickle', 'wb') as f:
    pickle.dump(LambdaProxy(L), f)

print("... lambdas are pickable!")
    