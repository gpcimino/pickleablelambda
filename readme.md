Pickable Lambda
===============

Makes lambda pickleable!

I want to thank Mike Müller from [Python Accademy](http://www.python-academy.com/) for the interesting discussion on
this topic and the smart ideas proposed to solve it!

Here is a simple example (see examples/simple_example.py):

```python
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

print("But if you import pickablelambda and you wrap L with pickable...")

from pickablelambda import pickable


with open('lambda.pickle', 'wb') as f:
    pickle.dump(pickable(L), f)

print("... lambdas are pickable!")
```

