from bs4 import BeautifulSoup

f = open('ntc8-cqa-tcdata/QUEST1500.xml')
data1 = f.read()  # ファイル終端まで全て読んだデータを返す
f.close()
soup = BeautifulSoup(data1, "html.parser")
all_q = soup.findAll('question_text')
for q in all_q:
    print(q.string, end="")
