#!/usr/bin/env python

import numpy as np
import chainer
from chainer import cuda, Function, gradient_check, Variable
from chainer import optimizers, serializers, utils
from chainer import Link, Chain, ChainList
import chainer.functions as F
import chainer.links as L

# Set data

X = np.loadtxt('question-x-num.txt').astype(np.float32)
Y = np.loadtxt('question-y-num.txt').astype(np.int32)
N = Y.size
index = np.arange(N)
#xtrain = X[index[index % 4 != 3],:]
#ytrain = Y[index[index % 4 != 3]]    #教師信号は整数値
xtest = X[index[index % 1 == 0],:]
yans = Y[index[index % 1 == 0]]

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
nrow, ncol = ans.shape
ok = 0
for i in range(nrow):
    cls = np.argmax(ans[i,:])
    #print(ans[i,:], cls)
    if cls == yans[i]:
        ok += 1
        if np.max(ans[i,:]) < 5 :
            print(i + 1, ": predict = ", cls, " answer = ", yans[i], " ○")
            print(ans[i,:], cls)

    else :
        print(i + 1, ": predict = ", cls, " answer = ", yans[i], " ×")
        print(ans[i,:], cls)

print(ok, "/", nrow, " = ", (ok * 1.0)/nrow)
