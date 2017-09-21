#!/usr/bin/env python

import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

# Set data (4.2)

X = np.loadtxt('question-x.txt').astype(np.float32)
Y = np.loadtxt('question-y.txt')
N = Y.size
Y2 = np.zeros(8 * N).reshape(N,8).astype(np.float32)
for i in range(N):
    Y2[i,Y[i]] = 1.0

index = np.arange(N)
xtrain = X[index[index % 2 != 0],:]
ytrain = Y2[index[index % 2 != 0],:] #教師信号、3次元ベクトル
xtest = X[index[index % 2 == 0],:]
yans = Y[index[index % 2 == 0]]
#(4.2)ここまで

# Define model(4.3)

class IrisChain(Chain): #Chainのクラスを設定する
    def __init__(self):
        super(IrisChain, self).__init__(
            l1=L.Linear(66,100), #Linearクラスで線形変換を行う
            l2=L.Linear(100,8),
        )

    def __call__(self,x,y):
        return F.mean_squared_error(self.fwd(x), y)
        # その値を二乗平均誤差の関数 F.mean_squared_error に渡して
        # 損失を求める

    def fwd(self,x):
         h1 = F.sigmoid(self.l1(x))
         # 出力を活性化関数 F.sigmoid に与える
         h2 = self.l2(h1)
         return h2

# Initialize model
#パラメータの学習 10000回パラメータを更新してパラメータを求める
model = IrisChain()
optimizer = optimizers.SGD()
optimizer.setup(model)

# Learn

for i in range(10000):
    x = Variable(xtrain)
    y = Variable(ytrain)
    model.zerograds()
    loss = model(x,y)
    loss.backward()
    optimizer.update()

# Test
# テストデータで評価
xt = Variable(xtest, volatile='on')
yy = model.fwd(xt)

ans = yy.data
nrow, ncol = ans.shape
ok = 0
for i in range(nrow):
    cls = np.argmax(ans[i,:])
    print((ans[i,:], cls))
    if cls == yans[i]:
        ok += 1
        print(i * 2 + 3, "=", cls)

print(ok, "/", nrow, " = ", (ok * 1.0)/nrow)
#nrow:テストデータの総数,ok:正解数なので、
#正解率が出力される
#(4.3)
