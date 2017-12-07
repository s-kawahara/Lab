述語項構造シソーラス 20141026版データについて 2016年1月8日　竹内孔一
(Predicate-Argument Structure Thesaurus)

シソーラスのデータの方を圧縮したデータです．
http://pth.cl.cs.okayama-u.ac.jp/vth/vths
ここのものと同じです．

ファイル:
  readme-PT.txt: このファイル
  pth日付-文字種.csv: シソーラス本体
  frame-文字種.csv: pth*.csvのAJ列にあるフレームidに対応したフレーム名

注意1: 文字コードはutf-8版とsjis版です．各カラムはカンマで区切られていて，各要素は二重引用符で
くくられています．格の指定などで，1つの要素の中にカンマを使って併記している例があるので
かならず二重引用符を１つの単位として処理して下さい．

注意2: frame*.csvでは括弧の半角・全角などで同じようなものがズレた表記になっています．
このあたりは後ほど修正します．

各列の詳細な説明というのはあまりないのですが，動詞だけのときの説明とほとんど同様です．
http://cl.cs.okayama-u.ac.jp/rsc/data
格1〜格5は作業の見やすさのためにわけた列で，深層格，表層格が意味役割体系です．

Webページで書いてるモノとすこし違うところがありますが，数は同じです．
異なる点
   本データ内　=>  Web 
1) 場所(時(点)) =>  時間(点)　時間関係がこれで今後Webの方に合わせる予定
   場所(時(間))，場所(時(毎))もあるが同様．基本的には，場所(時)にする予定
2) (?) という信頼度の低い無い場合に意味役割にマークが付いている

BCCWJの付与コーパスの公開が公開されています．BCCWJの利用アカウントが発行されると
https://bccwj-data.ninjal.ac.jp/mdl/
からdownloadできます．

ライセンスはMITライセンスです．
ご使用の際はなに述語シソーラス関連の発表を引用していただけるとありがたいです．
Webサイト: http://pth.cl.cs.okayama-u.ac.jp/

論文: Koichi Takeuchi, Kentaro Inui, Nao Takeuchi and Atsushi Fujita, A Thesaurus of Predicate-Argument Structure for Japanese Verbs to Deal with Granularity of Verb Meanings, The 8th Workshop on Asian Language Resources, pages 1-8, Beijing, 21th (21-22) August 2010.

どうぞよろしくお願いします．
------------------------------------------------------------
竹内　孔一 <koichi@cl.cs.okayama-u.ac.jp>
岡山大学大学院自然科学研究科
http://cl.cs.okayama-u.ac.jp/