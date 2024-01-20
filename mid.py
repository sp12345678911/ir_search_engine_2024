from os import listdir
from os.path import isfile, join
import math
import csv
import numpy as np


op = open('data/word1475.txt', mode='r', encoding="utf-8")
Keyword = []
IDF = {}
text = op.readlines()
for a in text:
    a = a.replace('\n', '')
    Keyword.append(a)
    IDF[a] = 0

path = './data'
files = listdir(path)
TFb = []
otherTFb = []
for filesA in files:
    fullpath = join(path, filesA)
    word_num = 0

    word_dic = {}

    if isfile(fullpath) and fullpath[-4:] == '.wrd':
        f = open('%s' % fullpath, mode='r')
        f_text = f.readlines()
        for wordc in f_text:
            wordc = wordc.replace('\n', '').split(' ')
            word_dic[wordc[0]] = int(wordc[1])
            word_num += int(wordc[1])

        TF = {}
        otherTF = []
        TFcalculate = []

        for wordd in Keyword:
            if wordd in word_dic:
                TF[wordd] = word_dic[wordd] / word_num
                otherTF.append(1)
                TFcalculate.append(TF[wordd])
            else:
                TF[wordd] = 0
                TFcalculate.append(TF[wordd])
                otherTF.append(0)
    else:
        continue

    TFb.append(TFcalculate)

    otherTFb.append(otherTF)

    for worde in word_dic:
        if worde in Keyword:
            IDF[worde] = IDF[worde] + 1


# def tf_txt(path, word, word_val):
#     f = open(path, mode='a', newline='')
#     writer = csv.writer(f)
#     writer.writerow([word, word_val])
#     f.close()


TFbnp = np.array(TFb)

IDFl = []
IDFb = []
for f in IDF:
    IDFl.append(math.log(10, 100 / IDF[f]))
IDFb.append(IDFl)

IDFbnp = np.array(IDFb)
print('IDF Array:')
print(IDFbnp)

TFIDF = TFbnp * IDFbnp
print('TF-IDF Array:')
print(TFIDF)

for g in TFIDF:
    f = open('weight1.txt', mode='a', newline='')
    writer = csv.writer(f)
    writer.writerow(g)
    f.close()
print('weight1 OK')

twoTFlinp = np.array(otherTFb)


twoTFli = twoTFlinp.tolist()
print('binary weight calculate OK')

for h in twoTFli:
    f = open('weight2.txt', mode='a', newline='')
    writer = csv.writer(f)
    writer.writerow(h)
    f.close()
print('weight2 OK')
