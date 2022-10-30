# This script runs hadoop Friends recommendation on selected file

sudo apt-get install unzip
unzip TP2-dataset.zip
export PATH=$PATH:/usr/local/hadoop/bin/
hdfs dfs -copyFromLocal soc-LiveJournal1Adj.txt input
hadoop com.sun.tools.javac.Main FriendRecommendation.java
jar cf wc.jar FriendRecommendation*.class
hadoop jar wc.jar FriendRecommendation input/soc-LiveJournal1Adj.txt output
hadoop fs -cat output/part-r-00000
cp output/part-r-00000 results/"result_friends"