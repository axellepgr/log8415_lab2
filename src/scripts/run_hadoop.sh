curl -k -L -s --compressed https://www.gutenberg.org/cache/epub/4300/pg4300.txt > pg4300.txt
export PATH=$PATH:/usr/local/hadoop/bin/
hdfs dfs -mkdir input
hdfs dfs -copyFromLocal pg4300.txt input
# mv ~/WordCount.java /usr/local/hadoop/sbin
hadoop com.sun.tools.javac.Main WordCount.java
jar cf wc.jar WordCount*.class
echo "\n Files available : \n"
hadoop fs -ls input/
echo "\nPlease select file : "
read file
hdfs dfs -rm output
hadoop jar wc.jar WordCount input/$file output
hadoop fs -cat output/part-r-00000