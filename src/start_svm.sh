. conf.sh
type=$1
feature_file=$DIR"./tmp_data/feature."$type
out_file=$DIR"./tmp_data/result."$type

cd $DIR/../liblinear/
./predict $feature_file model.res ./out
cd $DIR

cp $DIR/../liblinear/out $out_file
