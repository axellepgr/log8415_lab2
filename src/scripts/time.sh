#!/bin/bash

# This script runs WordCount program on Hadoop 3 times on all datasets and measures the execution time

FILES="input/*.txt"

export PATH=$PATH:/usr/local/hadoop/bin/
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

tar -czvf results.tar.gz results
mv results.tar.gz ~/
echo "Files processed. "