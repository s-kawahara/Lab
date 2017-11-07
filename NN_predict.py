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

def get_word(tree, chunk):
    surface = ''
    df3 = pd.read_table("question_word.txt")
    content = df3['question'].values
    for i in range(chunk.token_pos, chunk.token_pos + chunk.token_size):
        token = tree.token(i)
        features = token.feature.split(',')
        if token.surface in content:
            afters = tree.token(i+1).feature.split(',')
            if afters[0] == '助詞':
                surface += token.surface + ' ' + tree.token(i+1).surface
            else:
                surface += token.surface + ' ' + '空白'
        elif features[0] == '動詞':
            surface += features[6]
            break
    return surface

def get_2_words(line):
    cp = CaboCha.Parser('-f1')
    tree = cp.parse(line)
    chunk_dic = {}
    chunk_id = 0
    for i in range(0, tree.size()):
        token = tree.token(i)
        if token.chunk:
            chunk_dic[chunk_id] = token.chunk
            chunk_id += 1

    tuples = []
    for chunk_id, chunk in chunk_dic.items():
        if chunk.link > 0:
            from_surface = get_word(tree, chunk)
            to_chunk = chunk_dic[chunk.link]
            to_surface = get_word(tree, to_chunk)
            tuples.append(from_surface + ' ' + to_surface)
    return tuples


print("input:")
line = sys.stdin.readline()

tuples = get_2_words(line)
for t in tuples:
    list1 = t.split(' ')
    length = len(list1)
    if length == 3:
        nn_input = list1

if nn_input is None:
    print("疑問語と動詞の組が見つかりません。")
    sys.exit()
#nn_input = nn_inputs.rstrip().split(' ')

df = pd.read_table("input.txt")
df2 = pd.read_csv("pth20160108/pth20141026-sjis.csv", encoding="shift_jis", low_memory=False)
verb = nn_input[2]
verb_class = df2[df2["見出し語"] == verb]['大分類２'].values[0]

output = [0]
for num in range(1, 66):
    content = df[df.index == num].content.values[0]
    if content in nn_input:
        output.append(1)
    elif content == verb_class:
        output.append(1)
    else:
        output.append(0)
print(output)
# Set data

X = np.array(output).astype(np.float32)
xtest = np.reshape(X, (1, 66))

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
print("\noutput:\n", ans[0,:], cls)
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
    print('TIME')
elif cls == 6:
    print('NUMEX')
elif cls == 7:
    print('MONEY')
