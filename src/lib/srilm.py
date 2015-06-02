#!/usr/bin/env python
import sys
import re
 
class SRILm(object):
    def __init__(self, fp):
        self.ngram = {}
        self.orders={}
        self.order = 0
 
        line = fp.readline() # read the empty line
        while True:
            line = fp.readline().strip()
            if not line:
                break
 
            if line == "\\data\\":
                while True:
                    line = fp.readline().strip()
                    if line == "": break
 
                    m = re.compile("ngram (\d+)=(\d+)").search(line)
                    if m is not None:
                        self.orders[int(m.group(1))]= int(m.group(2))
                        #print >> sys.stderr, m.group(1)
                        #print >> sys.stderr, m.group(2)
                    #else:
                    #    print >> sys.stderr, "failed"
                    #    sys.exit(1)
 
            m=re.compile(r"\\(\d+)\-grams\:").match(line)
 
            if m is not None:
                #print m.group(1)
                while True:
                    line = fp.readline().strip()
                    if line == "": break
 
                    dices = line.split("\t")
                    f, gram = dices[:2]
                    gram = "$".join(gram.split())
 
                    if len(dices) > 2:
                        alpha = float(dices[2])
                    else:
                        alpha = 0.
 
                    self.ngram[gram] = [float(f), alpha]
 
    def log_prob(self, words):
        prev = "$".join(words)
        if prev not in self.ngram:
            if words[1] not in self.ngram or words[0] not in self.ngram:
                return -99.
            else:
                return self.ngram[words[0]][1]+self.ngram[words[1]][0]
        else:
            return self.ngram[prev][0]
 
    def __str__(self):
        ret = ""
        for order in self.orders:
            ret += "%d-gram: %d\n"% (order, self.orders[order])
        return ret
 
    def sentence_probability(self, sent):
        ret = 0.
        words = sent.strip().split()
        for i, word in enumerate(words):
            if i == 0:
                ret += self.log_prob(["<s>", word])
            else:
                ret += self.log_prob(words[i-1: i+1])
        return ret
 
if __name__=="__main__":
    print >> sys.stderr, "library is not runnable"
