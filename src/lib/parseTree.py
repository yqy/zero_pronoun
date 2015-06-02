import re
import nltk
def gen_tree(treestr):
	s=treestr[1:-1]
	t=s.strip().split(' ')
	key=t[0]
	value=t[1:]
	vs=[]
	for i in value:
		if i!='':
			vs.append(i)
	tree=nltk.Tree(key,vs)
	return tree
def is_a_tree(s):
	left=re.findall('<',s)
	right=re.findall('>',s)
	if len(left+right)==2:
		return 1
	else:
		return 0
	
def preProcess(s):
	#delete [], and change () into <>
	a=re.sub('[\[\d.\d\]]','',s)
	b=re.sub('\\(','<',a)
	c=re.sub('\\)','>',b)
	s=''
	for i in c:
		if i=='$':
			s+='D'
		else:
			s+=i
	return s
# input preprocessed syntactic tree String, output: treelebael	
def parseTree(c,treelabel):
	
	d=re.findall('<.*?>',c)
	
	treestrdic={}
	tree_name_dic={}
	
	num=1
	d_sub_temp=''
	for i in range(len(d)):
		temp=d[i]
		pos=0
		for j in range(len(temp)):
			if temp[j]=='<':
				pos=j
		treestr=temp[pos:]
		tree=gen_tree(treestr)
		treestrdic[treestr]=treelabel+str(num)
		tree_name_dic[treelabel+str(num)]=tree
		num+=1
	new=c
	old=c
	for key in treestrdic.keys():
		str_in_c=key
		sub_str=treestrdic[key]
		new=re.sub(str_in_c,sub_str,old)
		
		old=new
		
	
		
	return tree_name_dic,new
# determine  whther a tree is terminal tree
def is_terminal_leaf(tree,treedic):
	leaves=tree.leaves()
	# if tree is terminal tree,label=1, else label=0
	label=1
	for l in leaves:
		if l in treedic.keys():
			label=0
			break
	return label
#exchange substring to tree
def change_key_to_tree(tree,treedic):
	
	t=tree
	leaves=tree.leaves()
	new_leaves=[]
	for l in leaves: 
		if l in treedic.keys():
			ttree=treedic[l]
			new_leaves.append(ttree)
		else:
			new_leaves.append(l)
	return nltk.Tree(tree.node,new_leaves)

# get all subtree
def getFinalTree(treelist):
	treedic={}
	
	for i in treelist:
		for k in i.keys():
			treedic[k]=i[k]
			
	t_list=treedic.values()
	keys=treedic.keys()
	tree_list=[]
	
	new_tree_dic={}
	for key in treedic.keys():
		tree=treedic[key]
		label=is_terminal_leaf(tree,treedic)
		if label==1:
			new_tree_dic[key]=tree
	
	for i in range(len(treelist)):
		l_dic=treelist[i]
		for key in l_dic.keys():
			tree=l_dic[key]
			node=tree.node
			leaves=tree.leaves()
			new_leaves=[]
			for l in leaves:
				if l in new_tree_dic.keys():
					t=new_tree_dic[l]
					new_leaves.append(t)
				else:
					new_leaves.append(l)
			new_t=nltk.Tree(node,new_leaves)
			new_tree_dic[key]=new_t

	return new_tree_dic,treedic
# change the values in a dic into a list
def getvaluslist(equal_dic):
	valuselist=[]
	for k in equal_dic.keys():
		v=equal_dic[k]
		valuselist=valuselist+v
	return valuselist
# deleted redundancy subtree		
def del_redundancy(new_tree_dic):
	local_dic={}
	for k in new_tree_dic:
		newk=int(k)
		tree=new_tree_dic[k]
		local_dic[newk]=tree
	keylist=sorted(local_dic.keys())
	tup_list=[]
	for k in keylist:
		tup_list.append((k,local_dic[k]))
	equal_dic={}
	lastdic=equal_dic
	for i in range(len(tup_list)):
		existkey=getvaluslist(lastdic)
		k1=tup_list[i][0]
		t1=tup_list[i][1]
		if k1 in existkey:
			continue
		else:
			templist=[]
			if i<len(tup_list)-1:
				templist=tup_list[i+1:]
			for t in templist:
				
				k2=t[0]
				t2=t[1]
				if t1==t2:
					equal_dic.setdefault(k1,[])
					equal_dic[k1].append(k2)
		lastdic=equal_dic
		
	vlist=getvaluslist(equal_dic)
	finalkeys=equal_dic.keys()
	
	for k in local_dic.keys():
		if k not in vlist:
			if k not in equal_dic.keys() :
				finalkeys.append(k)
	finaltreelist=[]
	for k in finalkeys:
		finaltreelist.append(local_dic[k])
		
	return finaltreelist
def getSubTreeList(sent):
	c=preProcess(sent)
	iter=1
	new=c
	old=c
	treelist=[]
	
	while (is_a_tree(new)!=1 and iter<2000):
		tree_name_dic,new=parseTree(old,str(iter))
		treelist.append(tree_name_dic)
		old=new
		iter+=1
	if iter==1999:
		print 'NOTE: Error! Please check parseTree.getSubTreeList(sent)........'
	new_tree_dic,treedic=getFinalTree(treelist)
	finaltreelist=del_redundancy(new_tree_dic)
	return finaltreelist


if __name__=='__main__':
	sa='(ROOT [51.350] (SBARQ [45.930] (WHADVP [3.927] (WRB [3.862] Why)) (SQ [38.893] (VBZ [0.288] does) (NP [14.098] (DT [0.650] the) (NN [11.217] moon)) (VP [21.423] (VB [5.633] turn) (NP [13.756] (NN [11.170] orange))))))'
	
	
	
	
	
	
		
	
	
	
	
	
	