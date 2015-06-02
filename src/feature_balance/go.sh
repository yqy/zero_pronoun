#cat $1 | python feature_balance.py ./conf_svm.sh > tmp
cat $1 | python feature_balance.py ./conf.sh $2 > tmp
