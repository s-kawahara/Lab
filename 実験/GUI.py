#!/usr/bin/env python
# -*- coding: utf8 -*-
import sys
import tkinter

root = tkinter.Tk()
root.title(u"質問応答システム")
root.geometry("500x300")

#ラベル
Static1 = tkinter.Label(text=u'質問文を入力してください')
Static1.pack()

#エントリー
EditBox = tkinter.Entry(width=50)
EditBox.pack()

def GetValue(event):
    line = EditBox.get()
    Static3 = tkinter.Label(text=line)
    Static3.pack()

#ボタン
Button = tkinter.Button(text=u'質問')
line = Button.bind("<Button-1>",GetValue)
#左クリック（<Button-1>）されると，DeleteEntryValue関数を呼び出すようにバインド
Button.pack()
#Androidはどこが開発しましたか？
#芝浦工業大学はどこにありますか？
Static2 = tkinter.Label(text=u"質問文例\nAndroidはどこが開発しましたか？\n芝浦工業大学はどこにありますか？")
Static2.pack()


root.mainloop()
