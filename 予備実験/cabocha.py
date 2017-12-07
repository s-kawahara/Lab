import CaboCha
import pandas as pd

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

if __name__ == '__main__' :
    line = 'ウィンドウズ９８はどこが作りましたか？'
    tuples = get_2_words(line)
    for t in tuples:
        list1 = t.split(' ')
        length = len(list1)
        if length == 3:
            print(list1)
