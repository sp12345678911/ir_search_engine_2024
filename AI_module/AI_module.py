from collections import defaultdict
from os.path import isfile, join
import os
import numpy as np
import math
import csv


class Module:
    def __init__(self) -> None:
        self.keyword = self.generate_keyword()
        self.idf = defaultdict(int)
        self.tfb = []
        self.otherTFb = []
        self.TFcalculate = []
        self.current_path = os.getcwd()
        self.tfidf = []
        self.document_path = []
        self.parse_key_word()
        self.storge_weight()

    def generate_keyword(self):
        with open(r'data/word1475.txt', mode='r', encoding="utf-8") as op:
            temp = []
            for a in op.readlines():
                a = a.replace('\n', '')
                temp.append(a)
            return temp

    def parse_key_word(self):
        for file in os.listdir(f"{self.current_path}/data"):
            word_num = 0
            word_dic = {}
            fullpath = join(f"{self.current_path}/data", file)
            if isfile(f"{fullpath}"):
                if os.path.splitext(file)[1] == '.wrd':
                    self.document_path.append(file)
                    with open(f"{fullpath}", mode='r') as f:
                        for wordc in f.readlines():
                            wordc = wordc.replace('\n', '').split(' ')
                            word_dic.update({wordc[0]: int(wordc[1])})
                            word_num += int(wordc[1])
                        TF = defaultdict(int)
                        otherTF = []
                        TFcalculate = []

                        for wordd in self.keyword:
                            if wordd in word_dic:
                                TF[wordd] = word_dic[wordd] / word_num
                                otherTF.append(1)
                            else:
                                otherTF.append(0)
                            TFcalculate.append(TF[wordd])
                        self.tfb.append(TFcalculate)
                        self.otherTFb.append(otherTF)

            for worde in word_dic:
                if worde in self.keyword:
                    self.idf[worde] += 1

    def storge_weight(self):
        tfbnp = np.array(self.tfb)
        idfb = []
        idfl = []
        for f in self.idf:
            idfl.append(math.log(10, 100 / self.idf[f]))
        idfb.append(idfl)
        idfbnp = np.array(idfb)
        tfidf = tfbnp * idfbnp
        self.tfidf = tfidf.tolist()
        for g in tfidf:
            f = open('data\weight1.txt', mode='a', newline='')
            writer = csv.writer(f)
            writer.writerow(g)
            f.close()
        twoTFlinp = np.array(self.otherTFb)
        twoTFli = twoTFlinp.tolist()
        for h in twoTFli:
            f = open('data\weight2.txt', mode='a', newline='')
            writer = csv.writer(f)
            writer.writerow(h)
            f.close()


if __name__ == "__main__":
    m = Module()
    m.parse_key_word()
    m.storge_weight()

# # 打開全部的txt 然後維護好一個IDF 預設都為0 跟一個Keyword
# with open('word1475.txt', mode='r', encoding="utf-8") as op:
#     Keyword = []
#     IDF = defaultdict(int)
#     for a in op.readlines():
#         a = a.replace('\n', '')
#         Keyword.append(a)
#         # print(IDF[a])
#         # IDF[a] = 0


# TFb = []
# otherTFb = []


# TFbnp = np.array(TFb)
# IDFl = []
# IDFb = []
# for f in IDF:
#     IDFl.append(math.log(10, 100 / IDF[f]))
# IDFb.append(IDFl)

# IDFbnp = np.array(IDFb)
# print('IDF Array:')
# print(IDFbnp)

# TFIDF = TFbnp * IDFbnp
# print('TF-IDF Array:')
# print(TFIDF)

# for g in TFIDF:
#     f = open('weight1.txt', mode='a', newline='')
#     writer = csv.writer(f)
#     writer.writerow(g)
#     f.close()
# print('weight1 OK')

# twoTFlinp = np.array(otherTFb)


# twoTFli = twoTFlinp.tolist()
# print('binary weight calculate OK')

# for h in twoTFli:
#     f = open('weight2.txt', mode='a', newline='')
#     writer = csv.writer(f)
#     writer.writerow(h)
#     f.close()
# print('weight2 OK')
