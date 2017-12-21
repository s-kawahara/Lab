#!/usr/bin/env python
#coding:utf-8
import sys

import pandas as pd

f = open('verbs.txt', 'r')
line = f.readline().replace('\n','')

df2 = pd.read_csv("pth20160108/pth20141026-sjis.csv", encoding="shift_jis", low_memory=False)

while line:
    values = df2[df2["見出し語"] == line]['中分類'].values
    if len(values) > 0:
        verb_class = df2[df2["見出し語"] == line]['中分類'].values[0]
        #if  verb_class != verb_class:
        #    verb_class = df2[df2["見出し語"] == line]['中分類'].values[0]
    else:
        verb_class = "ないよおおおおおおおおおおお"
    print(verb_class)
    line = f.readline().replace('\n','')
f.close()
