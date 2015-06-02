import sys
raw_file = open(sys.argv[1])
test_file = open(sys.argv[2])
r = 0
r_in_r = 0
should = 0
no = "-1"
while True:
    line = raw_file.readline()
    if not line:break
    st = line.strip()
    line = test_file.readline()
    if not line:break
    an = line.strip()
    if not an == no:
        r += 1
        if st == an:
            r_in_r += 1
    if not st == no:
        should += 1
p = float(r_in_r)/float(r)
r = float(r_in_r)/float(should)
f = 2/(1/p+1/r)
print "P:%s"%p
print "R:%s"%r
print "F:%s"%f
    
