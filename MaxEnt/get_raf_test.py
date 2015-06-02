import sys
#f: mt result
#cat : raw result
f = open(sys.argv[1])
'''
while True:
    line = f.readline()
    if line.find("Summary") >= 0:
        break
while True:
    line = f.readline()
    if line.find("Summary") >= 0:
        break
'''
#begin useful info
al = 0
is_r = 0
r_in_r = 0
bad = "0" 
while True:
    line = sys.stdin.readline()
    if not line:break
    oo = line.strip()
    line = line.strip().split("\t")
    re = line[1].split(" ")[0]
    line = f.readline()
    line = line.strip().split("\t")
    freq = 0.0
    r = ""
    for i in range(1,len(line)/2 + 1):
        if float(line[i*2]) > (freq):
        #if float(line[i*2]) > (freq)-0.6:
            freq = float(line[i*2])
            r = line[i*2-1]
    print re,r

    if not re.find(bad) >= 0:
        al += 1
        if not r.find(bad) >= 0:
            if re == r:
                is_r += 1
    if not r.find(bad) >= 0:
        r_in_r += 1
#        print oo
#    print al
print al
print is_r
print r_in_r
R = float(float(is_r)/float(al))
P = float(float(is_r)/float(r_in_r))
F = float(2)/(1/P+1/R)
print "R:%f"%R
print "P:%f"%P
print "F:%f"%F
