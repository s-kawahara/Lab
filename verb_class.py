#!/usr/bin/env python
#coding:utf-8
import sys

import pandas as pd

f = open('verbs.txt', 'r')
line = f.readline().replace('\n','')

df = pd.read_table("input.txt")
df2 = pd.read_csv("pth20160108/pth20141026-sjis.csv", encoding="shift_jis", low_memory=False)

while line:
    values = df2[df2["見出し語"] == line]['大分類２'].values
    if len(values) > 0:
        verb_class = df2[df2["見出し語"] == line]['大分類２'].values[0]
    else:
        verb_class = "ないよおおおおおおおおおおお"
    print(verb_class)
    line = f.readline().replace('\n','')
f.close()
