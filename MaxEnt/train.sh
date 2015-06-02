input=$1
bin/mallet import-file --input $1 --output ./data/yqy.train.data

bin/mallet train-classifier --input ./data/yqy.train.data --output-classifier ./data/yqy.classifier --trainer MaxEnt 
