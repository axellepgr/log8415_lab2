#! /bin/bash
export PATH=$PATH:/usr/local/hadoop/bin
hdfs dfs -mkdir input
for k in 0 1 2
do
    mkdir output_of_time$k
    mkdir times$k
done
for i in 0 1 2 3 4 5 6 7 8
do
    hdfs dfs -copyFromLocal ~/text$i.txt input
done
for j in 0 1 2
do
    for i in 0 1 2 3 4 5 6 7 8
    do
        { time hadoop jar wc.jar WordCount input/text$i.txt output ; } 2>> output_of_time$j/text$i.txt
    done
    for i in 0 1 2 3 4 5 6 7 8
    do
        tail -n 3 output_of_time$j/text$i.txt > times$j/text$i.txt
    done
done
hdfs dfs -rm -r output/
hdfs dfs -rm -r input/