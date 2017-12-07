#!/usr/bin/env python

import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

# Set data

X = np.loadtxt('question-x_309.txt').astype(np.float32)
Y = np.loadtxt('question-y_309.txt').astype(np.int32)
N = Y.size
index = np.arange(N)
xtrain = X[index[index % 1 == 0],:]
ytrain = Y[index[index % 1 == 0]]    #教師信号は整数値
#xtest = X[index[index % 4 == 3],:]
#yans = Y[index[index % 4 == 3]]

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

# Initialize model

model = MyChain()
optimizer = optimizers.SGD()
optimizer.setup(model)

# Learn

n = 309
bs = 4
for j in range(2000):
    sffindx = np.random.permutation(n)
    for i in range(0, n, bs):
        x = Variable(xtrain[sffindx[i:(i+bs) if (i+bs) < n else n]])
        y = Variable(ytrain[sffindx[i:(i+bs) if (i+bs) < n else n]])
        model.zerograds()
        loss = model(x,y)
        loss.backward()
        optimizer.update()


model.to_cpu() # CPUで計算できるようにしておく
serializers.save_npz("309model.npz", model) # npz形式で書き出し
