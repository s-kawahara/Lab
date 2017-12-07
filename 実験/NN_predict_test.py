#!/usr/bin/env python
import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L
import sys

import pandas as pd
import CaboCha
import matplotlib.pyplot as plt

# Define model

class MyChain(Chain):
    def __init__(self):
        super(MyChain, self).__init__(
            l1=L.Linear(78,100),
            l2=L.Linear(100,10),
        )

    def __call__(self,x,y):
        return F.softmax_cross_entropy(self.fwd(x), y)

    def fwd(self,x):
         h1 = F.sigmoid(self.l1(x))
         h2 = self.l2(h1)
        #h3 = F.softmax(h2) :順伝播の最後にsoftmax関数必要なし
         return h2

print("input:")
line = sys.stdin.readline()
output = line.split()
#print(output)
# Set data

X = np.array(output).astype(np.float32)
xtest = np.reshape(X, (1, 78))

# Initialize model

model = MyChain()
optimizer = optimizers.SGD()
optimizer.setup(model)
serializers.load_npz("309model.npz", model) # "mymodel.npz"の情報をmodelに読み込む

# Test

xt = Variable(xtest, volatile='on')
yy = model.fwd(xt)

ans = yy.data
cls = np.argmax(ans[0,:])
#print("\noutput:\n", ans[0,:], cls)
print("\nquestion_type:")
if cls == 0:
    print('PERSON')
elif cls == 1:
    print('ORGANIZATION')
elif cls == 2:
    print('LOCATION')
elif cls == 3:
    print('ARTIFACT')
elif cls == 4:
    print('DATE')
elif cls == 5:
    print('NUMEX')
elif cls == 6:
    print('MONEY')
elif cls == 7:
    print('REASON')
elif cls == 8:
    print('METHOD')
elif cls == 9:
    print('STATE')
plt.plot(ans[0,:])
plt.xticks([0,1,2,3,4,5,6,7,8,9], ["人","組織","場所","人工物","日付","数量","金額","理由","方法","状態"])
plt.show()
