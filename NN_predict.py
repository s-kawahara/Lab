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

nn_inputs = sys.stdin.readline()
nn_input = nn_inputs.rstrip().split(' ')

df = pd.read_table("input.txt")

output = [0]
for num in range(1, 66):
    content = df[df.index == num].content.values[0]
    if content in nn_input:
        output.append(1)
    else:
        output.append(0)

# Set data

X = np.array(output).astype(np.float32)
xtest = np.reshape(X, (1, 66))

# Define model

class MyChain(Chain):
    def __init__(self):
        super(MyChain, self).__init__(
            l1=L.Linear(66,100),
            l2=L.Linear(100,8),
        )

    def __call__(self,x,y):
        return F.softmax_cross_entropy(self.fwd(x), y)

    def fwd(self,x):
         h1 = F.sigmoid(self.l1(x))
         h2 = self.l2(h1)
        #h3 = F.softmax(h2) :順伝播の最後にsoftmax関数必要なし
         return h2

# Initialize model

model = MyChain()
optimizer = optimizers.SGD()
optimizer.setup(model)
serializers.load_npz("109model.npz", model) # "mymodel.npz"の情報をmodelに読み込む

# Test

xt = Variable(xtest, volatile='on')
yy = model.fwd(xt)

ans = yy.data
cls = np.argmax(ans[0,:])
print(ans[0,:], cls)

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
    print('TIME')
elif cls == 6:
    print('NUMEX')
elif cls == 7:
    print('MONEY')
