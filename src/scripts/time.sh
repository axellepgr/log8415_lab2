hdfs dfs -rm output
echo "\n Files available : \n"
hadoop fs -ls input/
echo "\nPlease select file : "
read file
time hadoop jar wc.jar WordCount input/$file output