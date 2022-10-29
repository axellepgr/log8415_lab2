hdfs dfs -rm -r output/
rm -r results/
mkdir results
mkdir results/hadoop
mkdir results/linux
for f in $FILES
do
        file=$(basename "$f")
        echo "Processing $file"
        touch result_$file
        for i in 1 2 3
        do
                # HADOOP
                { time hadoop jar wc.jar WordCount input/$file output ; } 2>> result_$file
                tail -n 3 result_$file >> results/hadoop/r_$file
                # LINUX
                { time ./wordcount_linux.sh input/$file ; } &>> result_$file
                tail -n 3 result_$file >> results/linux/r_$file
        done
        rm result_$file
done
echo "Files processed. "