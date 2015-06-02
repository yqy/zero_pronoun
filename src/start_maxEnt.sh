. conf.sh
type=$1
feature_file=$DIR"./tmp_data/feature."$type
out_file=$DIR"./tmp_data/result."$type

cd $DIR/../MaxEnt/
bin/mallet classify-file --input $feature_file --output - --classifier ./data/classifier.$type > ./result.test
cd $DIR

cp $DIR/../MaxEnt/result.test $out_file
