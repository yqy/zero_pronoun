#coding=utf8
import parseTree
import nltk
import math
import sys

def get_tree_list(filename):
	fin=file(filename)
	lines=[line for line in fin]
	fin.close()
	sent_list=[]
	for line in lines:
		if line[0:11]=='<ParseTree>':
			sent_list.append(line[11:].strip())
	#print sent_list
	treelist=[]
	for s in sent_list:
		tr=parseTree.getSubTreeList(s)
		treelist.append(tr)
	return treelist

#input  subtree fragment list of one sentence
#output: the syntactic tree of one sentence
def find_sent_tree(treelist):
	tree=treelist[0]
        #print tree
        #print "*"
	for t in treelist:
		if t.height()>tree.height():
			tree=t
        #                print tree
        #                print "*"
	return tree

#input  subtree fragment list of one sentence
#output: all node in a syntactic tree of one sentence
def find_nodes(subfragmentslist):
	nodes=[t.node for t in subfragmentslist]
	return nodes
def get_nodes(tree):
	nodes=[tree.node]
	subtrees=[]
	level=tree.height()
	while level>1:
		subtrees+=get_subtrees_of_a_tree(tree)

#input onetree
#output get subtrees list
def get_subtrees_of_a_tree(one_tree):
	subtrees=[t for t in one_tree]
	return subtrees

#input: a tree
#output: 1: is terminal tree with 2 levels, 0 not a terminal tree with more than 2 levels
def is_terminal_tree(tree):
	if type(tree)==type('str'):
		return 'yes'
	else:
		if tree.height()>2:
			return 'no'
		else:
			return 'yes'
def get_next_level_subtrees(subtreeslist):
	next_level_subtrees=[]
	subtrees=[]
	for t in subtreeslist:
		sub_ts=get_subtrees_of_a_tree(t)
		for st in sub_ts:
			subtrees.append(st)
			is_termianl=is_terminal_tree(st)
			if is_termianl=='no':
				next_level_subtrees.append(st)
	return next_level_subtrees,subtrees
def get_all_subtrees(tree):
	print ' in get all subtree'
	if type(tree)==type('str'):
		return []
	else:
		level=tree.height()
		print level
		allsubtrees=[tree]
		subtreelist=[tree]
		while level>1:
			print 'level='+str(level)
			next_level_subtrees,subtrees=get_next_level_subtrees(subtreelist)
			subtreelist=next_level_subtrees
			allsubtrees+=subtrees
			level-=1
		return allsubtrees

	
class oneTree:
	def __init__(self,tree):
		self.tree=tree
		self.namelist=[]
		self.name_subtree_dic={}
		self.name_depth_dic={}
		self.name_size_dic={}
		self.name_weight_dic={}
		self.parent_child_dic={}
		self.name_production={}
		self.terminal_subtree_list=[]
		self.multi_level_subtree_list=[]
	def get_subtree_values(self):
		if type(self.tree)==type('str'):
			self.namelist=['0']
			self.name_subtree_dic['0']=self.tree
			self.name_depth_dic['0']=1
			self.name_size_dic['0']=0
			self.parent_child_dic['0']=''
			
		else:
			name='11'
			parentnodes=[name]
			self.namelist=['11']
			self.name_subtree_dic['11']=self.tree
			self.name_depth_dic['11']=1
                        #print self.tree.productions()
			#self.tree.productions存着树的信息，结点，边，根
                        size=len(self.tree.productions())
			height=self.tree.height()
			self.name_size_dic['11']=size
			subtreelist=[self.tree]
			depth=1
			while height>1:
				depth+=1
				next_level_subtrees,subtrees=get_next_level_subtrees(subtreelist)
				for i in range(len(subtrees)):
					name=str(depth)+str(i+1)
					self.namelist.append(name)
					self.name_subtree_dic[name]=subtrees[i]
					self.name_depth_dic[name]=depth
					size=len(subtrees[i].productions())
					self.name_size_dic[name]=size
				subtreelist=next_level_subtrees
				height-=1
			for name in self.name_subtree_dic.keys():
				tree=self.name_subtree_dic[name]
				subtrees=[t for t in tree]
				for i in range(len(subtrees)):
					s1=subtrees[i]
					for subname in self.name_subtree_dic.keys():
						s2=self.name_subtree_dic[subname]
						if s1==s2:
							self.parent_child_dic.setdefault(name,[])
							self.parent_child_dic[name].append(subname)
					
	def get_subtree_weight(self,lamda,mu):
		for name in self.namelist:
			size=self.name_size_dic[name]
			depth=self.name_depth_dic[name]
			weight=math.pow(math.sqrt(lamda),size)*math.pow(math.sqrt(mu),depth)
			self.name_weight_dic[name]=weight
			
	def get_productions(self):
		for name in self.multi_level_subtree_list:
			tree=self.name_subtree_dic[name]
			node=tree.node
			sub_nodes=[t.node for t in tree]
			pro=nltk.Tree(node,sub_nodes)
			self.name_production[name]=pro
	def get_terminalsubtrees(self):
		for name in self.namelist:
			tree=self.name_subtree_dic[name]
			if tree.height()==2:
				self.terminal_subtree_list.append(name)
			else:
				self.multi_level_subtree_list.append(name)
	def one_fun(self):
		self.get_subtree_values()
		self.get_terminalsubtrees()
		self.get_productions()
				
class subtree:
	def __init__(self,CT,name):
		self.CT=CT
		self.name=name
		self.subtree=CT.name_subtree_dic[name]
		self.depth=CT.name_depth_dic[name]
		self.size=CT.name_size_dic[name]
		self.production=[]
		
		self.is_terminaltree=''
		self.children=[]
		self.is_terminalTree()
		self.getChildren()
		if name in CT.name_production.keys():
			self.production=CT.name_production[name]
	def is_terminalTree(self):
		if self.name in self.CT.terminal_subtree_list:
			self.is_terminaltree='yes'
		else:
			self.is_terminaltree='no'
	def getChildren(self):
		if self.name in self.CT.parent_child_dic.keys():
			namelist=self.CT.parent_child_dic[self.name]
			self.children=[subtree(self.CT,n) for n in namelist]
		else:
			self.children=[]
def c(s1,ct1,s2,ct2,lamda):
	if s1.subtree.node!=s2.subtree.node:
		return 0
	elif s1.is_terminaltree=='yes' and s2.is_terminaltree=='yes':
		if s1.subtree.leaves()==s2.subtree.leaves():
			return 1
		else:
			return lamda
	else:
		if s1.production!=s2.production:
			return 0
		else:
			s1_children=s1.children
			s2_children=s2.children
			if len(s1_children)!=len(s2_children):
				print 'error'
				return ''
			else:
				templist=[(1+c(s1_children[i],ct1,s2_children[i],ct2,lamda)) for i in range(len(s2_children))]
				result=lamda
				for t in templist:
					result*=t
				return result
#dynamic programming reference: nltk chapter 6 structured programing algorithm design.
def c2(s1,ct1,s2,ct2,lamda,lookup={}):
	keyname=s1.name+s2.name
	if keyname not in lookup.keys():
		if s1.subtree.node!=s2.subtree.node:
			lookup[keyname]=0
			
		elif s1.is_terminaltree=='yes' and s2.is_terminaltree=='yes':
			if s1.subtree.leaves()==s2.subtree.leaves():
				lookup[keyname]= 1
			else:
				lookup[keyname]= lamda
		else:
			if s1.production!=s2.production:
				lookup[keyname]= 0
			else:
				s1_children=s1.children
				s2_children=s2.children
				if len(s1_children)!=len(s2_children):
					print 'error'
					return ''
				else:
					templist=[(1+c(s1_children[i],ct1,s2_children[i],ct2,lamda)) for i in range(len(s2_children))]
					result=lamda
					for t in templist:
						result*=t
					lookup[keyname]= result
	return lookup[keyname]
def tree_kernel(ct1,ct2,lamda,mu):
	#lookup={}
	n1_list=[subtree(ct1,ct1.namelist[i]) for i in range(len(ct1.namelist))]
	n2_list=[subtree(ct2,ct2.namelist[i]) for i in range(len(ct2.namelist))]
	sim=0
	for s1 in n1_list:
		for s2 in n2_list:
			t=0
			d1=s1.depth
			d2=s2.depth
			para=(d1+d2)*0.5
			t=c(s1,ct1,s2,ct2,lamda)
			sim+=math.pow(mu,para)*t
	return sim
			
def tree_similarity(ct1,ct2,lamda,mu):
	s12=tree_kernel(ct1,ct2,lamda,mu)
	s1=tree_kernel(ct1,ct1,lamda,mu)
	s2=tree_kernel(ct2,ct2,lamda,mu)
	d1122=s1*s2
	
	sim=0
	if d1122!=0:
		sim=s12/math.sqrt(d1122)
	return sim

#tree.height(): root=1, leaf= height how many levels in this tree 
#len(tree) how many subtree of this tree
# 
def TreeKernelDemo():
	#tree kernel betwee How far is it from Denver to Aspen ? and What county is Modesto , California in ?
	s= str(sys.argv[0])
	slist=s.split('\\')
	d=''
	for s in slist[0:-1]:
		d+=s+'\\'
		
	filename=d+'ParesTreeStrings.txt'
	aaa=get_tree_list(filename)# read data from file
	
	subtree1_list=aaa[0] # get subtrees of the 1st sentence
	subtree2_list=aaa[1] # get subtress of the 2nd sentence
	#print '1:',subtree1_list
	#print '2:',subtree2_list
	sent_tree1=find_sent_tree(subtree1_list) # get root tree of the 1st sentence
        print sent_tree1
	sent_tree2=find_sent_tree(subtree2_list) # get root tree of the 2nd sentence
	
	
	ct1=oneTree(sent_tree1)
	ct1.one_fun()
	
	
	ct2=oneTree(sent_tree2)
	ct2.one_fun()
		
	
	lamda=0.1 #set parameter lamda
	mu=0.9 # set parameter mu
	
	s=tree_similarity(ct1,ct2,lamda,mu)
	print 'the similarity is :' , str(s)
	return subtree1_list,subtree1_list
if __name__=='__main__':
	
	a=TreeKernelDemo()
	
	
	

	
	


	
	
	
