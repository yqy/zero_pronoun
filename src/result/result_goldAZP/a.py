import sys
st = open(sys.argv[1])
predict = open(sys.argv[2])
rank = open(sys.argv[3])

error_all = 0
error_rank = 0
error_predict = 0
error_only_predict = 0
error_only_rank = 0
error_refresh = 0
all = 0
while True:
    st_line = st.readline()
    if not st_line:break
    st_line = st_line.strip()
    predict_line = predict.readline().strip()
    rank_line = rank.readline().strip()
    all += 1
    pre = False
    if st_line == predict_line:
        pre = True
    ran = False
    if rank_line == st_line:
        ran = True
    if not ran and not pre:
        error_all += 1
    if not ran:
        error_rank += 1
    if not pre:
        error_predict += 1
    if not pre and ran:
        error_only_predict += 1
    if not ran and pre:
        error_only_rank += 1
print "error_all",error_all
print "error_rank",error_rank
print "error_predict",error_predict
print "error_only_predict",error_only_predict
print "error_only_rank",error_only_rank

    
