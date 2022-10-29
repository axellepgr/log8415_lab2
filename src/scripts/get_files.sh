#!/bin/bash

# This script retrieves the files and puts them into the input/ folder

input_file="experiment_files.txt"
export PATH=$PATH:/usr/local/hadoop/bin/
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
hdfs dfs -mkdir input
echo "Getting 9 files ..."
i=0
cr=$'\r'
while IFS= read -r line
do
    i=$((i+1))
    line="${line%$cr}"
    echo "$i. $line"
    curl -k -L -s --compressed $line > $i.txt
    hdfs dfs -copyFromLocal $i.txt input
    rm $i.txt
done < $input_file
echo -e "\nFiles are in the input folder."