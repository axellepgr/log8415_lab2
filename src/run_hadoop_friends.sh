sudo apt-get install unzip
unzip TP2-dataset.zip
export PATH=$PATH:/usr/local/hadoop/bin/
# hdfs dfs -mkdir input
hdfs dfs -copyFromLocal soc-LiveJournal1Adj.txt input
# mv ~/WordCount.java /usr/local/hadoop/sbin
hadoop com.sun.tools.javac.Main FriendRecommendation.java
jar cf wc.jar FriendRecommendation*.class
echo "\n Files available : \n"
hadoop fs -ls input/
echo "\nPlease select file : "
read file
hadoop jar wc.jar FriendRecommendation input/$file output
hadoop fs -cat output/part-r-00000