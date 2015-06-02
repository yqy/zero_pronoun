#coding=utf8
import sys
from bs4 import BeautifulSoup
import re
sys.path.append("./lib/")
import get_dir

def add_azp(sentence,parse):
    out_sentence = []
    parse_items = parse.split(" ")
    word_index = 0
    out_parse = []
    is_pro = False
    word_need_add = []
    ad = ""
    for item in parse_items:
        if re.match("^.+?\)+$",item):
            word_index += 1
        else:
            pass
        is_pro = False
        if item.find("*") >= 0:
            is_pro = True
        out_parse.append(item)
    word_index = 0
    for line in sentence.split("\n"):
        line = line.strip()
        if re.match("^<.+?>$",line):
            out_sentence.append(line.strip())
        else:
            words = line.strip().split(" ")
            for word in words:
                if word_index in word_need_add:
                    out_sentence.append("*add*")
                word_index += 1
                out_sentence.append(word)
    return "\t".join(out_sentence)," ".join(out_parse)

def main():

    path = sys.argv[1]
    out_type = sys.argv[2]   
 
    file_list = get_dir.get_all_file(path,[])
    for files in file_list:
        files_name = ".".join(files.split(".")[:-1])
        files_tag = files.split(".")[-1]
        if files_tag == "coref":
            file_coref = open(files_name+".coref")
            file_parse = open(files_name+".parse")
            while True:
                line = file_coref.readline()
                if not line:break
                line = line.strip()
                if not (line.startswith("<DOC") or line.startswith("<TEXT") or line.endswith("DOC>") or line.endswith("TEXT>")):
                    print >> sys.stderr, line 
                    sentence = line
                    parse = ""
                    while True:
                        line = file_parse.readline()
                        line = line.strip()
                        if len(line) == 0:
                            break
                        parse = parse + " " + line.strip()
                    soup = BeautifulSoup(sentence)
                    sentence = soup.prettify().encode("utf8").strip()
                    sentence,parse = add_azp(sentence,parse)
                    if out_type == "sentence":
                        print sentence.strip()
                    else:
                        print parse.strip()
if __name__ == "__main__":
    main()
