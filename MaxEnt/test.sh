input=$1
bin/mallet classify-file --input $input --output - --classifier ./data/yqy.classifier > ./result.test
cat $1 | python get_raf_test.py ./result.test


