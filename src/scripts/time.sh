#!/bin/bash

FILES="input/*.txt"

export PATH=$PATH:/usr/local/hadoop/bin/
hdfs dfs -rm -r output/
mkdir results
for f in $FILES
do
        file=$(basename "$f")
        echo "Processing $file"
        touch result_$file
        for i in 1 2 3
        do
                { time hadoop jar wc.jar WordCount input/$file output ; } 2>> result_$file
                tail -n 2 result_$file > tmp
                head -n 1 tmp >> results/r_$file
                rm tmp
        done
        rm result_$file
done
echo "Files processed. "