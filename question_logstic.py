#!/usr/bin/env python

import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

# Set data

X = np.loadtxt('question-x.txt').astype(np.float32)
Y = np.loadtxt('question-y.txt')
N = Y.size
Y2 = np.zeros(8 * N).reshape(N,8).astype(np.float32)
for i in range(N):
    Y2[i,Y[i]] = 1.0

index = np.arange(N)
xtrain = X[index[index % 2 != 0],:]
ytrain = Y2[index[index % 2 != 0],:]
xtest = X[index[index % 2 == 0],:]
yans = Y[index[index % 2 == 0]]

# Define model

class IrisRogi(Chain):
    def __init__(self):
        super(IrisRogi, self).__init__(
            l1=L.Linear(66,8),   #Linearクラスで線形変換を行う
        )

    def __call__(self,x,y):
        return F.mean_squared_error(self.fwd(x), y)
        # その値を二乗平均誤差の関数 F.mean_squared_error に渡して
        # 損失を求める

    def fwd(self,x):
        return F.softmax(self.l1(x))

# Initialize model

model = IrisRogi()
optimizer = optimizers.Adam()
optimizer.setup(model)

# Learn

n = 65
bs = 15
for j in range(5000):
    sffindx = np.random.permutation(n)
    for i in range(0, n, bs):
        x = Variable(xtrain[sffindx[i:(i+bs) if (i+bs) < n else n]])
        y = Variable(ytrain[sffindx[i:(i+bs) if (i+bs) < n else n]])
        model.zerograds()
        loss = model(x,y)
        loss.backward()
        optimizer.update()

# Test

xt = Variable(xtest, volatile='on')
yy = model.fwd(xt)

ans = yy.data
nrow, ncol = ans.shape
ok = 0
for i in range(nrow):
    cls = np.argmax(ans[i,:])
    print(ans[i,:], cls)
    if cls == yans[i]:
        ok += 1

print(ok, "/", nrow, " = ", (ok * 1.0)/nrow)
# nrow:テストデータ、okは正解数
