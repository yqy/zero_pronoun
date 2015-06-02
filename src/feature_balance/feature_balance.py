import sys
import random
#read conf
conf = {}
f = open(sys.argv[1])
while True:
    line = f.readline()
    if not line:break
    line = line.strip()
    if line.startswith("#"):
        continue
    line = line.split("=")
    conf[line[0].strip()] = line[1].strip().strip('"') 

if len(sys.argv) > 2:
    conf["ratio"] = sys.argv[2].strip() 

result_index = int(conf["result_index"])
pos_list = []
neg_list = []
pos_num = 0
neg_num = 0
num = 0
neg = conf["bad"]

while True:
    line = sys.stdin.readline()
    if not line:break
    line = line.strip().split(conf["split"])
    result = line[result_index]
    content = conf["split"].join(line[int(result_index):]) 
    if result.find(neg) >= 0:
        neg_list.append(content) 
        neg_num += 1
    else:
        pos_list.append(content)
        pos_num += 1
ratio = float(conf["ratio"])
right_pos_num = int(neg_num/ratio)
copy_time = int(right_pos_num/pos_num)
print >> sys.stderr, pos_num,neg_num,copy_time
copy_pos_list = []
for i in range(copy_time):
    copy_pos_list += pos_list
pos_num = len(copy_pos_list)
need_pos_num = neg_num/ratio - pos_num
for feature in pos_list:
    rand_num = random.randint(1,len(pos_list)) 
    if rand_num < need_pos_num:
        copy_pos_list.append(feature)
pos_num = len(copy_pos_list)
pos_list = copy_pos_list 
out_list = pos_list + neg_list
out_list = random.sample(out_list,len(out_list))
if conf["need_num"] == "1":
    for feature in out_list:
        print "%d%s%s"%(num,conf["split"],feature) 
        num += 1
else:
    for feature in out_list: 
        print "%s"%(feature) 
