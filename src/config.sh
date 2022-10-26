sed -i 's/# export JAVA_HOME=/export JAVA_HOME=\/usr\/lib\/jvm\/java-11-openjdk-amd64\//' /usr/local/hadoop/etc/hadoop/hadoop-env.sh
cd /usr/local/hadoop/sbin
# install Java, maybe no need ?
yes | sudo apt-get update && sudo apt-get install openjdk-11-jdk
# Solving key problems
cd ~/.ssh
echo | ssh-keygen -P ''
cat id_rsa.pub >> authorized_keys
# start 
cd /usr/local/hadoop/sbin
./start-dfs.sh
cd ~/.ssh
export HADOOP_INSTALL=/usr/local/hadoop && export PATH=$HADOOP_INSTALL/bin:$PATH
export PATH=$PATH:/usr/local/hadoop/bin/
curl https://www.gutenberg.org/cache/epub/4300/pg4300.txt > pg4300.txt
hdfs dfs -mkdir input
hdfs dfs -copyFromLocal pg4300.txt input
mv ~/WordCount.java /usr/local/hadoop/sbin
# Pas fini j'y travaille
# hadoop com.sun.tools.javac.Main WordCount.java
# jar cf wc.jar WordCount*.class
# echo "\n Files available : \n"
# hadoop fs -ls input/

# echo "\nPlease select file : "
# read file
# hadoop jar wc.jar WordCount input/$file output
# hadoop fs -cat output/part-r-00000

# # Get Spark
# curl https://archive.apache.org/dist/spark/spark-2.0.0/spark-2.0.0.tgz > spark-2.0.0.tgz