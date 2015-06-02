#coding=utf8
import sys
import os
sys.path.append("./lib/")
import buildTree
from srilm import SRILm
from get_feature import *
from word2vec import *
from numpy import linalg
from numpy import array

def read_result(filename,t,neg):
    result = []
    score = []
    f = open(filename)
    while True:
        line = f.readline()
        if not line:break
        line = line.strip().split("\t")
        if line[1].find(neg) >= 0:
            pos_freq = float(line[4])
            if pos_freq >= t: 
                result.append("1")
                score.append(pos_freq)
            else:
                result.append("0")
                score.append(float(line[2]))
        else:
            if line[3].find(neg) >= 0:
                pos_freq = float(line[2])
                if pos_freq >= t: 
                    result.append("1")
                    score.append(pos_freq)
                else:
                    result.append("0")    
                    score.append(float(line[4]))
    return result,score


def read_result_svm(filename,t,neg):
    result = []
    score = []
    f = open(filename)

    while True:
        line = f.readline()
        if not line:break
        line = line.strip()
        s = float(line)
        re = "0"   
        if s >= t:
            re = "1"
        result.append(re)    
        score.append(s)
    return result,score



def main():
    parse = open(sys.argv[2])
    sentence = open(sys.argv[1])
    lm = SRILm(open("./dict/model.srilm", "r"))
    f = open("./dict/HcP")
    HcP = []
    while True:
        line = f.readline()
        if not line:break
        line = line.strip()
        HcP.append(line)
    f.close()


    Max = 3
    candidates_list = []
    dependency_list = []
    wl_list = []

    azp_t = 0.5
    combine_t = 0.5

    ####
    res_t = 0.5
    res_rank_t = -9.9
    ###

    iter_times = 1
    neg = "0"

    FeatureFile = "./tmp_data/feature."

    sentence_index = 0

    result_gold = open("./result/result.gold","w")
    result_rank = open("./result/result.rank","w")

    w2v = Word2Vec("../data/word2vec")
    print >> sys.stderr, "word2vec done!"

    while True:
    
        #for test log
        #while True:
        #    line = sys.stdin.readline()
        #    break

        line = parse.readline() 
        if not line:break
        line = line.strip()
        if len(line) >= 1600:
            line = sentence.readline()
            continue
        nl,wl = buildTree.buildTree(line)

        #dependency
        fw = open("./dependency/p","w")
        fw.write(line.decode("utf8").encode("gbk").replace("*","").replace("-","").replace("TOP","")[1:-1].strip()+"\n")
        fw.close()

        dependency = {}

        cmd = "./go_depenend.sh > t"
        os.system(cmd)
        fr = open("./dependency/result")
        if len(fr.readlines()) < 1:
            line = sentence.readline()
            continue
        fr.close()

        fr = open("./dependency/result")
        index = 0
        while True:
            line = fr.readline()
            if not line:break
            line = line.strip()
            if not line:break
            line = line.strip().decode("gbk").encode("utf8").split("\t")
            dependency[index] = int(line[2]) - 1
            index += 1

        line = sentence.readline()
        print >> sys.stderr,sentence_index,line.strip()
        sentence_index += 1
        resolution_list_sentence = buildTree.get_resolution_info(line.strip())
        resolution_list_parse = buildTree.get_np(nl) 
        zps,candidates = buildTree.get_resolution_pair(resolution_list_sentence,resolution_list_parse,wl) 

        candidates_list.append(candidates)
        if len(candidates_list) > Max:
            candidates_list = candidates_list[1:]

        dependency_list.append(dependency)
        if len(dependency_list) > Max:
            dependency_list = dependency_list[1:]

        wl_list.append(wl)
        if len(wl_list) > Max:
            wl_list = wl_list[1:]

        feature_list = get_azp_feature(zps,candidates_list)
        write_feature_file(FeatureFile+"azp",feature_list,sentence_index)

        index = 0
        for feature in feature_list:
            if feature[0].find(neg) >= 0:
                zps[index].is_zp = False
            index += 1 
        new_zps = []
        for zp in zps:
            if zp.is_zp:
                new_zps.append(zp)  
        zps = new_zps

        feature_list = get_res_feature(zps,candidates_list,wl,lm,dependency_list,wl_list,HcPz,PcPz,HcP,dependency)
        
        candi_num = 0
        candi_list = []
        candi_vec_list = [] #存放candi的vector
        for candidates in candidates_list:
            for candi in candidates:
                candi_num += 1
                candi_list.append(candi.tag)

                cs = toString(candi.nodes).split("_")
                candi_vec = array([0.0001]*100)
                add_num = 0
                for c in cs:
                    cv = w2v.get_vector(c)
                    if cv:
                        candi_vec += array(cv)
                        add_num += 1
                if add_num >= 1:
                    candi_vec = candi_vec/add_num
                candi_vec_list.append(list(candi_vec))


        index = 0
        zp_norm = [0]* candi_num
        fl = []    
        while True:
            if index >= len(feature_list):
                break
            feature = feature_list[index]
            fl.append(feature)
            index += 1
            if index % candi_num == 0: #一个zp到次数
                write_feature_file_svm(FeatureFile+"res",fl,sentence_index)
              
                cmd = "./start_svm.sh res > ./tmp_data/t"
                os.system(cmd)
                result_file = "./tmp_data/result.res"
                class_result,score = read_result_svm(result_file,res_t,neg)

                i = 0 
                for point in score:
                    zp_norm[i] += point 
                    i += 1

                fl = []

        zp_norm_point = []
        for p in zp_norm:
            zp_norm_point.append(p/float(len(feature_list)/candi_num + 1))        

        index = 0
        rank_result = []
        gold_result = []
        fl = []    
        while True:
            if index >= len(feature_list):
                break
            feature = feature_list[index]
            fl.append(feature)
            index += 1
            if index % candi_num == 0:
                write_feature_file_svm(FeatureFile+"res",fl,sentence_index)
              
                cmd = "./start_svm.sh res > ./tmp_data/t"
                os.system(cmd)
                result_file = "./tmp_data/result.res"
                class_result,score = read_result_svm(result_file,res_t,neg)

                rank_list = []

                freq = 0.0
                res_target = "-1"
                gold_target = "-1" 
                i = 0 
                for point in score:
                    if not fl[i][0].find(neg) >= 0: #是正例
                        gold_target = candi_list[i]
                    if point >= freq: #best first
                        freq = point 
                        res_target = candi_list[i] 
                    relation_list = []
                    this_candi_vector = candi_vec_list[i]
                    for candi_vec in candi_vec_list:
                        relation_list.append(cosin(this_candi_vector,candi_vec))
                    rank_list.append((point,relation_list))
                    i += 1
                gold_result.append(gold_target)

                rank_score = []
                rank_score_for_iteration = []
                rank_index = 0
                for (score,rl) in rank_list:
                    point = 0.0
                    norm = 0.0
                    for i in range(len(rl)):
                        point += rl[i]*rank_list[i][0]
                        norm += abs(rl[i])
                        if i == rank_index:
                            point -= rl[i]*rank_list[i][0]
                            norm -= abs(rl[i])
                    add_score = point
                    if not norm == 0:
                        add_score = point/norm

                    rank_score.append(add_score)
                    rank_score_for_iteration.append(0.0)
                    rank_index += 1                

                op = res_rank_t
                oc = "-1"
                i = 0
                for rank_point in rank_score:
                    raw_point = rank_list[i][0]
                    point = rank_point + 0.9*raw_point
                    if point >= op:
                        oc = candi_list[i]
                        op = point
                    i += 1
                
                if zps[(index-1)/candi_num].is_zp:
                    rank_result.append(oc)
                else:
                    rank_result.append("-1")
                fl = []

        for result in gold_result:
            result_gold.write(result+"\n")
        for result in rank_result:
            result_rank.write(result+"\n")
    print >> sys.stderr,"Done !!!!!"

if __name__ == "__main__":
    main()
