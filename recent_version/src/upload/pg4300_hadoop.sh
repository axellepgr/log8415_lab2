#! /bin/bash
export PATH=$PATH:/usr/local/hadoop/bin
hdfs dfs -mkdir input
curl -O https://www.gutenberg.org/cache/epub/4300/pg4300.txt
hdfs dfs -copyFromLocal ~/pg4300.txt input
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wcpg4300.jar WordCount*.class
{ time hadoop jar wcpg4300.jar WordCount input output ; } 2>> pg4300_hadoop_output.txt
tail -n 3 pg4300_hadoop_output.txt >> pg4300_hadoop_time.txt
rm pg4300_hadoop_output.txt
rm 'WordCount$TokenizerMapper.class'
rm 'WordCount$IntSumReducer.class'
rm WordCount.class && rm WordCount.java
hdfs dfs -rm -r output/
hdfs dfs -rm -r input/
