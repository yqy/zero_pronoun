#coding=utf8
import sys
import re
class Node:
    tag = None
    parent = None
    index = -1
    word = ""
    child = []
    right = None
    left = None
    def __init__(self,parent=None,word="",tag="",index=-1):
        self.parent = parent
        self.word = word
        self.tag = tag
        self.child = []
        self.index = index
        self.right = None
        self.left = None
    def has_child(self,n):
        if n in self.child:
            return True
        return False
    def add_child(self,child):
        self.child.append(child)
    def get_leaf(self):
        nl = []
        for c in self.child:
            if c.index >= 0:
                nl.append(c)
            else:
                nl += c.get_leaf()
        return nl
    def get_pub_node(self,node):
        #获得当前节点和node的公共父节点
        if not node:
            return None
        father = node.parent
        while True:
            if not father:break
            sf = self.parent
            while True:
                if not sf:break
                if sf == father:
                    return father
                sf = sf.parent
            father = father.parent
        return None

class Stack:
    items = []
    def __init__(self,items=[]):
        self.items = items
    def push(self,item):
        self.items.append(item)
    def size(self):
        return len(self.items)
    def pop(self):
        if len(self.items) > 0:
            last = self.items[-1]
            self.items = self.items[:-1]
            return last
        else:
            return None
    def last(self):
        if len(self.items) > 0:
            return self.items[-1]
        else:
            return None
    def combine(self):
        return self.items

def print_node_list(nl):
    for n in nl:
        if n.parent:
            print "******"
            print n.index,n.word,n.tag,n.parent.tag
            print "child:"
            for q in n.child:
                print q.tag,
            print
        else:
            print "******"
            print n.index,n.word,n.tag,"None"
            print "child:"
            for q in n.child:
                print q.tag,
            print

def buildTree(parse):
    stack = Stack([])
    item = ""
    parent = None
    left = None
    right = None
    nl = []
    wl = []
    word_index = 0
    for letter in parse.decode("utf8"):
        if letter == "(":
            if len(item.strip()) > 0:
                item = item.strip().encode("utf8")
                item = item.split(" ")
                word = ""
                tag = ""
                index = -1
                if len(item) == 2:
                    tag = item[0].strip()
                    word = item[1].strip()
                    index = word_index
                    word_index += 1
                else:
                    tag = item[0].strip()
                node = Node(parent,word,tag,index)

                if len(item) == 2:
                    node.left = left
                    wl.append(node)
                    if node.left:
                        node.left.right = node
                    left = node

                if node.parent:
                    node.parent.add_child(node)
                stack.push(parent)
                parent = node
                nl.append(node)
                item = ""
        elif letter == ")":
            if len(item.strip()) > 0:
                item = item.strip().encode("utf8")
                item = item.split(" ")
                word = ""
                tag = ""
                index = -1
                if len(item) == 2:
                    tag = item[0].strip()
                    word = item[1].strip()
                    index = word_index
                    word_index += 1
                else:
                    tag = item[0].strip()
                node = Node(parent,word,tag,index)

                if len(item) == 2:
                    node.left = left
                    wl.append(node)
                    if node.left:
                        node.left.right = node
                    left = node

                if node.parent:
                    node.parent.add_child(node)
                nl.append(node)
                item = ""
            else:
                last = stack.pop()
                parent = last
        else:
            item += letter
    return nl,wl 

class ResolutionItem:
    nodes = []
    head = -1
    tail = -1
    tag = "0"
    is_zp = False
    def __init__(self,nodes=[],head=-1,tail=-1,tag="0",is_zp=False):
        self.nodes = nodes
        self.head = head
        self.tail = tail
        self.tag = tag
        self.is_zp = is_zp

    def show(self):
        print "***"
        print "is_zp:",self.is_zp
        print "tag:",self.tag
        print self.head,self.tail
        for node in self.nodes:
            print node.word,
        print 

    def size(self):
        return self.tail-self.head+1
    def res(self,ri):
        if not self.tag=="0":
            if self.tag == ri.tag:
                return True
        return False
    def eqaul(self,ri):
        if self.head >= 0 and self.tail >= 0:
            if self.head == ri.head and self.tail == ri.tail:
                return True
        return False

def is_zero_pronoun(word):
    if word.find("*") >= 0:
        return True
    else:
        return False

def get_resolution_info(sentence):
    words = sentence.split("\t")

    resolution_stack = []
    resolution_list = []

    index = -1
    for word in words:
        if re.match("^\<coref.+?\>$",word):
            tag = re.findall('id=\"(.+?)\"',word)
            ri = ResolutionItem([],index+1,-1,tag[0],False)
            resolution_stack.append(ri)

        elif re.match("^\</coref.*?\>$",word):
            ri = resolution_stack[-1]
            ri.tail = index
            resolution_stack = resolution_stack[:-1]
            resolution_list.append(ri)
        else:
            index += 1
            
    return resolution_list
        
def get_np(node_list):
    resolution_list = []
    for node in node_list:
        if node.tag.startswith("NP"):
            if node.parent:
                if node.parent.tag.startswith("NP"):
                    continue
            nl = node.get_leaf()
            ri = ResolutionItem(nl,nl[0].index,nl[-1].index,"0",False)
            if not (ri.size() == 1 and is_zero_pronoun(ri.nodes[0].word)):
                resolution_list.append(ri)
        else:
            if node.tag == "-NONE-" and is_zero_pronoun(node.word):
                ri = ResolutionItem([node],node.index,node.index,"0",True)
                resolution_list.append(ri)
    return resolution_list

def get_resolution_pair(resolution_list_sentence,resolution_list_parse,wl): 
    zp = []
    candidates = []
    for ri in resolution_list_sentence:
        if ri.size() == 1:
            if is_zero_pronoun(wl[ri.head].word):
                ri.is_zp = True
                ri.nodes.append(wl[ri.head])
                zp.append(ri)
    for ri in resolution_list_parse:            
        has_before = False
        for rii in resolution_list_sentence:
            if ri.eqaul(rii):
                ri.tag = rii.tag
                has_before = True
                break
        if ri.is_zp:
            if not has_before:
                zp.append(ri)
        else:       
            candidates.append(ri)
    return zp,candidates
