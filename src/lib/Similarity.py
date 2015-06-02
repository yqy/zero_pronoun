#coding=utf8
#import StanfordParser
from tree_kernel import *
#import parseTree

def getsim_by_str(s1,s2):
    #print 'calculating similairity...'
    subtree1_list=parseTree.getSubTreeList(s1)
    subtree2_list=parseTree.getSubTreeList(s2)
    #print subtree1_list 
    #get Tree
    sent_tree1=find_sent_tree(subtree1_list) # get root tree of the 1st sentence
    sent_tree2=find_sent_tree(subtree2_list) #
    #print type(sent_tree1)
    #print sent_tree1 
    #创建对象oneTree
    ct1=oneTree(sent_tree1)
    ct1.one_fun()
    ct2=oneTree(sent_tree2)
    ct2.one_fun()
    lamda=0.1 #set parameter lamda
    mu=0.9 # set parameter mu
    
    s=tree_similarity(ct1,ct2,lamda,mu)
    #print 'the similarity is :' , str(s)
    return s,sent_tree1,sent_tree2

def getTree(sent):
    s1=StanfordParser.StanfordParser(sent)
    subtree1_list=parseTree.getSubTreeList(s1)
    sent_tree1=find_sent_tree(subtree1_list)
    return sent_tree1

if __name__=='__main__':
    #sent1='How far is it from Denver to Aspen'
    #sent2='What county is Modesto , California in'
    #s,sent_tree1,sent_tree2=getsim(sent1,sent2)
    s1 = "(TOP (IP-HLN (NP-SBJ (NP (NP (NP-PN (NR 天津港)) (NP (NN 保税区))) (DP (DT 各) (CLP (M 项))) (NP (NN 经济) (NN 指标))) (NP (NN 增幅))) (VP (VV 居) (QP-OBJ (NP-PN (NR 中国)) (QP (OD 首) (CLP (M 位)))))))"
    s2 = "(TOP (FRAG (NN 新华社) (NR 天津) (NT 一月) (NT 十日) (NN 电) (PU （) (NN 记者) (NR 满学杰) (NN 通讯员) (NR 张红) (PU ）)))"
    s,sent_tree1,sent_tree2=getsim_by_str(s1,s2)
    
