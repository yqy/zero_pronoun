#coding=utf8
import sys
from numpy import linalg
from numpy import array
from numpy import inner
def cosin(Al,Bl):
    A = array(Al)
    B = array(Bl)
    nA = linalg.norm(A)
    nB = linalg.norm(B)
    if nA == 0 or nB == 0:
        return 0
    num = inner(A,B)
    denom = nA * nB
    cos = num / denom
    #sim = 0.5 + 0.5 * cos #归一化
    sim = cos
    return sim


class Word2Vec:
    word_dict = {}
    def __init__(self,w2v_dir):
        f = open(w2v_dir)
        line = f.readline()
        while True:
            line = f.readline()
            if not line:break
            line = line.strip().split(" ")
            word = line[0]
            vector = line[1:]
            vec = [float(item) for item in vector]
            self.word_dict[word] = vec
    def get_vector(self,word):
        if word in self.word_dict:
            return self.word_dict[word]
        else:
            return None

if __name__ == "__main__":
    main()
