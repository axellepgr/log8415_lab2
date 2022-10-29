export PATH=$PATH:/usr/local/hadoop/bin/
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
echo "\n Files available : \n"
hadoop fs -ls input/
echo "\nPlease select file : "
read file
hdfs dfs -rm -r output/
hadoop jar wc.jar WordCount input/$file output
hadoop fs -cat output/part-r-00000
mkdir results
mkdir results/hadoop
cp output/part-r-00000 results/hadoop/"result_$file"