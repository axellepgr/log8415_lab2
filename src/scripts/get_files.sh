#!/bin/bash

input_file="experiment_files.txt"
export PATH=$PATH:/usr/local/hadoop/bin/

curl -k -L -s --compressed https://www.gutenberg.org/cache/epub/4300/pg4300.txt > pg4300.txt
hdfs dfs -mkdir input
hdfs dfs -copyFromLocal pg4300.txt input
rm pg4300.txt
echo "Getting 9 files ..."
i=0
cr=$'\r'
while read -r line
do
    i=$((i+1))
    line="${line%$cr}"
    echo "$i. $line"
    curl -k -L -s --compressed $line > $i.txt
    hdfs dfs -copyFromLocal $i.txt input
    rm $i.txt
done < $input_file
echo -e "\nFiles are in the input folder."