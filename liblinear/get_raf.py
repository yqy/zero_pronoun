import sys
#f: mt result
# ff: st result
for i in range(10):
    f = open(sys.argv[1])
    ff = open(sys.argv[2])
    al = 1
    is_r = 1
    r_in_r = 1
    bad = "0" 
    thresh = i/10.0
    while True:
        line = ff.readline()
        if not line:break
        oo = line.strip()
        line = line.strip().split(" ")
        re = line[0]
        line = f.readline()
        line = line.strip().split(" ")
        freq = 0.0
        r = line[0].strip()
        r = float(line[0])
        if r >= thresh:
            r = "1"
        else:
            r = "0"
    
        if not re.find(bad) >= 0:
            al += 1
            if not r.find(bad) >= 0:
                if re == r:
                    is_r += 1
        if not r.find(bad) >= 0:
            r_in_r += 1
    #        print oo
    #    print al
    print thresh
    print al
    print is_r
    print r_in_r
    R = float(float(is_r)/float(al))
    P = float(float(is_r)/float(r_in_r))
    F = float(2)/(1/P+1/R)
    print "R:%f"%R
    print "P:%f"%P
    print "F:%f"%F
    f.close()
